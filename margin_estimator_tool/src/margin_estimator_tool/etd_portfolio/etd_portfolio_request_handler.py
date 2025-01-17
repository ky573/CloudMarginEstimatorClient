"""
This module contains logic for retrieving information about products from
endpoint and then outputting them in desired form.
"""


import csv
import json
from typing import Dict, Any
import os
import click
from cpme_api.models import BodyEstimator
import cpme_api.models as spec
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.export_context import ExportContext
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.csv_export_strategy import CSVExportStrategy
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.excel_export_strategy import ExcelExportStrategy
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.json_export_strategy import JSONExportStrategy
from margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base import RequestHandler
from margin_estimator_tool.src.margin_estimator_tool.core.utils import flatten_dict

# study https://deutsche-boerse-risk.github.io/CloudPrismaMarginEstimator/docs/gui.html#prepare-etd-portfolio


class EtdPortfolioRequestHandler(RequestHandler):
    """Handler for sending requests to the /estimator endpoint and exporting data."""

    REQUIRED_HEADERS = "Product ID,Contract Date,Call Put Flag,Exercise Price,Version Number,Net LS Balance"

    def __init__(self,
                 csv_file,
                 date=None,
                 version=None,
                 timestamp=None,
                 to_excel=False,
                 to_json=False,
                 export_dir=None,
                 ):
        super().__init__()
        self.csv_file = csv_file
        self.business_date = self._get_business_date(date, version)
        self.version = version == "LIVE"
        self.timestamp = timestamp
        self.to_excel = to_excel
        self.to_json = to_json
        self.export_dir = export_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    def process_and_provide_output(self) -> None:
        """Processes the data from /estimator and exports it according to the specified format."""
        if not self._validate_header():
            return

        portfolio = self.send_request()
        # flatten_dict(portfolio)
        #
        # print(json.dumps(portfolio, indent=4))
        #
        # context = ExportContext()
        #
        # if self.to_excel:
        #     context.set_strategy(ExcelExportStrategy("portfolio"))
        # elif self.to_json:
        #     context.set_strategy(JSONExportStrategy("portfolio"))
        # else:
        #     context.set_strategy(CSVExportStrategy("portfolio"))
        #
        # context.export_data(str(self.business_date), self.version, portfolio, self.export_dir)

        flattened_data = []
        if isinstance(portfolio, dict):
            # Handle single portfolio item
            flattened_data.append(flatten_dict(portfolio))
        elif isinstance(portfolio, list):
            # Handle multiple portfolio items
            flattened_data = [flatten_dict(item) for item in portfolio]
        else:
            click.echo("Error: Invalid portfolio data structure")
            return

        context = ExportContext()

        if self.to_excel:
            context.set_strategy(ExcelExportStrategy("portfolio"))
        elif self.to_json:
            context.set_strategy(JSONExportStrategy("portfolio"))
        else:
            context.set_strategy(CSVExportStrategy("portfolio"))

        context.export_data(str(self.business_date), self.version, flattened_data, self.export_dir)

        click.echo(f"Portfolio exported to {self.export_dir}")

    def send_request(self) -> Dict[str, Any]:
        """Sends a POST request to /estimator endpoint with provided portfolio."""
        request_body = self._setup_request_body()
        try:
            response = self.api.estimator_post(body=request_body.to_dict())
            print(json.dumps(response, indent=4))
            self._check_for_error_in_response(response)
            return response
        except Exception as e:
            self._handle_request_error(e)
        return {}

    def _validate_header(self) -> bool:
        """Validates the CSV file headers against the required format."""
        try:
            with open(self.csv_file, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader, None)
                if headers is None:
                    raise ValueError("CSV file is empty.")

                headers_str = ",".join(headers)
                if headers_str != self.REQUIRED_HEADERS:
                    raise ValueError(f"Headers mismatch. Expected: '{self.REQUIRED_HEADERS}', Found: '{headers_str}'.")

            click.echo("Headers validated successfully.")
            return True
        except (ValueError, FileNotFoundError) as e:
            click.echo(f"Error validating CSV headers: {e}")
            return False

    def _setup_request_body(self) -> BodyEstimator:
        """Sets up the body for the POST request to /estimator endpoint."""
        request_body = BodyEstimator()
        request_body.snapshot = spec.Snapshot()
        request_body.snapshot.live = self.version
        request_body.snapshot.business_date = self.business_date
        request_body.snapshot.live_timestamp = self.timestamp
        request_body.clearing_currency = 'EUR'

        etd_csv_comp = spec.BodyEstimatorPortfolioComponents()
        print(self._load_portfolio())
        etd_csv_comp.etd_csv = spec.EtdCsv(csv=self._load_portfolio())

        request_body.portfolio_components.append(etd_csv_comp)
        return request_body

    def _load_portfolio(self) -> str:
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            return f.read()

