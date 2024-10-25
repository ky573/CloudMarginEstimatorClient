from typing import Dict, Any, Optional
from margin_estimator_tool.margin_calculator.export_strategy.export_context import ExportContext
from margin_estimator_tool.margin_calculator.export_strategy.csv_export_strategy import CSVExportStrategy
from margin_estimator_tool.margin_calculator.export_strategy.excel_export_strategy import ExcelExportStrategy
from margin_estimator_tool.margin_calculator.export_strategy.json_export_strategy import JSONExportStrategy
from .request_handler_base import RequestHandler
import requests
import click


class ProductsRequestHandler(RequestHandler):
    """Handler for sending requests to the /products endpoint and exporting data."""

    def __init__(self, date: Optional[str], version: Optional[str], filters: Optional[str], to_excel: bool,
                 to_json: bool, export_dir: str):
        super().__init__()
        self.date = date
        self.version = version
        self.filters = self._parse_filters(filters)
        self.to_excel = to_excel
        self.to_json = to_json
        self.export_dir = export_dir

    def _parse_filters(self, filter_str: Optional[str]) -> Dict[str, str]:
        """Parses the filter string into a dictionary."""
        if filter_str:
            return dict(f.split(':') for f in filter_str.split(','))
        return {}

    def send_request(self) -> Dict[str, Any]:
        """Sends a GET request to the /products endpoint with optional filters, date, and version."""
        # params = filter params

        try:
            response = self.api.products_get()
            return response
        except requests.exceptions.HTTPError as e:
            click.echo(f"HTTP Error: {e}", err=True)
        except requests.exceptions.RequestException as e:
            click.echo(f"Error sending request: {e}", err=True)
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
        return {}

    def process_and_export(self) -> None:
        """Processes the data from /products and exports it according to the specified format."""
        products = self.send_request()

        context = ExportContext()

        if self.to_excel:
            context.set_strategy(ExcelExportStrategy())
        elif self.to_json:
            context.set_strategy(JSONExportStrategy())
        else:
            context.set_strategy(CSVExportStrategy())

        context.export_data(products, self.export_dir)
