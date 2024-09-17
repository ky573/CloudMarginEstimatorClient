import os
import click
import requests
import plotly.graph_objects as go
from openpyxl import Workbook
from datetime import datetime, timedelta
import json
from cpme_api.api import CpmeApi, Configuration, fancy
from cpme_api.api.feature.utils import csv_to_str
import cpme_api.models as spec
from cpme_api.models import set_data_validation


class MarginCalculator:
    def __init__(self, api):
        self.api = api
        self.initial_margins = []
        self.dates = []
        self.margin_details = []

    # def load_portfolio(self):
    #     """Loads portfolio data from a CSV file."""
    #     try:
    #         with open('estimator_etd_csv.csv', 'r') as f:
    #             return f.read()
    #     except FileNotFoundError:
    #         raise click.BadParameter("Portfolio file 'estimator_etd_csv.csv' not found.")
    #     except Exception as e:
    #         raise click.BadParameter(f"Error loading portfolio file: {e}")

    def post_request(self, es_body):
        """Sends a POST request to the specified URL with the given headers and data."""
        try:
            response = self.api.estimator_post(body=es_body.to_dict())
            return response
        except requests.exceptions.HTTPError as e:
            click.echo(f"HTTP Error: {e}", err=True)
        except requests.exceptions.RequestException as e:
            click.echo(f"Error sending request: {e}", err=True)
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
        return {}

    def extract_data(self, business_date, data):
        """Extracts and aggregates initial margin data from the API response."""
        self.initial_margins.append(data['portfolio_margin'][0]['initial_margin'])
        self.dates.append(business_date)

        # Store margin details for export
        self.margin_details.append({
            "business_date": business_date,
            "portfolio_margin": data.get('portfolio_margin'),
            "drilldowns": data.get('drilldowns')
        })

    def save_graph(self, export_dir):
        """Saves the initial margin graph to a file."""
        formatted_dates = [datetime.strptime(str(date), "%Y%m%d") for date in self.dates]

        fig = go.Figure(data=go.Scatter(x=formatted_dates, y=self.initial_margins, mode='lines+markers'))
        fig.update_layout(
            title='Initial Margin Over Time',
            xaxis_title='Date',
            yaxis_title='Initial Margin (EUR)',
            xaxis=dict(
                tickformat='%Y-%m-%d',
                type='date'
            )
        )

        fig.write_image(f"{export_dir}/initial_margin_graph.jpeg")
        click.echo(f"Graph saved to {export_dir}/initial_margin_graph.jpeg")

    def flatten_dict(self, d, parent_key='', sep='_'):
        """Flattens nested dictionaries and lists into a single level dictionary for easy Excel export."""
        items = []
        for k, v in d.items():
            new_key = f'{parent_key}{sep}{k}' if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Convert list to a string or handle first element if it's a dict for simplicity
                if len(v) > 0 and isinstance(v[0], dict):
                    for idx, sub_item in enumerate(v):
                        items.extend(self.flatten_dict(sub_item, f'{new_key}_{idx + 1}', sep=sep).items())
                else:
                    items.append((new_key, str(v)))
            else:
                items.append((new_key, v))
        return dict(items)

    def create_workbook(self):
        """Creates an Excel workbook and initializes portfolio and drilldowns sheets."""
        wb = Workbook()
        ws1 = wb.active
        ws1.title = "portfolio_margin"
        ws2 = wb.create_sheet(title="drilldowns")
        return wb, ws1, ws2

    def prepare_headers(self):
        """Prepares headers for portfolio and drilldowns sheets."""
        portfolio_headers = set()
        drilldown_headers = set()

        # Extract headers by examining all data entries
        for detail in self.margin_details:
            for portfolio in detail["portfolio_margin"]:
                flat_portfolio = self.flatten_dict(portfolio)
                portfolio_headers.update(flat_portfolio.keys())

            for drilldown in detail["drilldowns"]:
                flat_drilldown = self.flatten_dict(drilldown)
                drilldown_headers.update(flat_drilldown.keys())

        # Convert headers to lists and add 'business_date'
        portfolio_headers = ['business_date'] + sorted(list(portfolio_headers))
        drilldown_headers = ['business_date'] + sorted(list(drilldown_headers))
        return portfolio_headers, drilldown_headers

    def populate_sheet(self, ws, headers, data_key):
        """Populates a given worksheet with data based on the specified headers."""
        ws.append(headers)

        for detail in self.margin_details:
            business_date = detail["business_date"]
            for item in detail[data_key]:
                flat_item = self.flatten_dict(item)
                row = [business_date] + [flat_item.get(header, '') for header in headers[1:]]
                ws.append(row)

    def save_workbook(self, wb, export_dir):
        """Saves the workbook to the specified directory."""
        excel_path = f"{export_dir}/margin_details.xlsx"
        wb.save(excel_path)
        click.echo(f"Excel file saved to {excel_path}")

    def export_to_excel(self, export_dir):
        """Coordinates the export of margin details to an Excel file."""
        wb, ws1, ws2 = self.create_workbook()
        portfolio_headers, drilldown_headers = self.prepare_headers()

        self.populate_sheet(ws1, portfolio_headers, "portfolio_margin")
        self.populate_sheet(ws2, drilldown_headers, "drilldowns")

        self.save_workbook(wb, export_dir)

    def is_business_day(self, current_date):
        """Check if the current date is a weekend."""
        return current_date.weekday() not in [5, 6]

    def setup_estimator_body(self):
        """Sets up the body of request."""
        es_body = spec.BodyEstimator()
        es_body.snapshot = spec.Snapshot()
        es_body.snapshot.live = True
        es_body.clearing_currency = 'EUR'

        etd_csv_comp = spec.BodyEstimatorPortfolioComponents()
        etd_csv_comp.etd_csv = spec.EtdCsv(csv=csv_to_str("estimator_etd_csv.csv"))

        es_body.portfolio_components.append(etd_csv_comp)

        return es_body

    def run(self, date_from, date_to, export_dir):
        """Main function to run the margin calculation."""
        start_date = datetime.strptime(date_from, "%Y%m%d")
        end_date = datetime.strptime(date_to, "%Y%m%d")

        es_body = self.setup_estimator_body()

        current_date = start_date
        while current_date <= end_date:
            if self.is_business_day(current_date):
                business_date = int(current_date.strftime("%Y%m%d"))
                # es_body.snapshot.business_date = business_date
                data = self.post_request(es_body)
                print(json.dumps(data, indent=4))

                if data == {}:
                    click.echo(f"Error sending request for {business_date}. Exiting.")
                    break

                self.extract_data(business_date, data)

            current_date += timedelta(days=1)

        self.save_graph(export_dir)
        self.export_to_excel(export_dir)


def check_click_arguments(date_from, date_to, export_dir):
    """Check if the click arguments are valid."""
    try:
        datetime.strptime(date_from, "%Y%m%d")
        datetime.strptime(date_to, "%Y%m%d")
    except ValueError:
        raise click.BadParameter("Date format must be YYYYMMDD.")

    if not os.path.exists(export_dir):
        raise click.BadParameter(f"Export directory '{export_dir}' not found.")


def setup_api():
    set_data_validation(False)
    config = Configuration()
    config.api_key = "9c40a29c-8b1d-4245-b3d9-2ffe5b5e9358"
    config.proxy = 'http://webproxy.deutsche-boerse.de:8080'
    config.enable_logging = True
    api = CpmeApi(configuration=config)
    return api


@click.command()
@click.option('--date_from', required=True, type=str, help='Start date in YYYYMMDD format')
@click.option('--date_to', required=True, type=str, help='End date in YYYYMMDD format')
@click.option('--export_dir', required=True, type=click.Path(), help="Directory to save the graph and Excel file.")
def main(date_from, date_to, export_dir):
    """Main function to run the margin calculation."""
    check_click_arguments(date_from, date_to, export_dir)
    api = setup_api()
    calculator = MarginCalculator(api)
    calculator.run(date_from, date_to, export_dir)
    api.close()


if __name__ == '__main__':
    main()
