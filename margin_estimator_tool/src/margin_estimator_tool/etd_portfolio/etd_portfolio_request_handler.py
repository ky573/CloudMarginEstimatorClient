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
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.json_export_strategy import JSONExportStrategy
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.etd_portfolio_csv_export_strategy import EtdPortfolioCSVExportStrategy
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.etd_portfolio_excel_export_strategy import EtdPortfolioExcelExportStrategy
from margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base import RequestHandler


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

        context = ExportContext()

        file_suffix = "portfolio"

        if self.to_excel:
            context.set_strategy(EtdPortfolioExcelExportStrategy(file_suffix))
        elif self.to_json:
            context.set_strategy(JSONExportStrategy(file_suffix))
        else:
            context.set_strategy(EtdPortfolioCSVExportStrategy(file_suffix))

        context.export_data(str(self.business_date), self.version, portfolio, self.export_dir)

        click.echo(f"Portfolio exported to {self.export_dir}")

    def send_request(self) -> Dict[str, Any]:
        """Sends a POST request to /estimator endpoint with provided portfolio."""
        request_body = self._setup_request_body()
        try:
            response = self.api.estimator_post(body=request_body.to_dict())
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
        etd_csv_comp.etd_csv = spec.EtdCsv(csv=self._load_portfolio())

        request_body.portfolio_components.append(etd_csv_comp)
        return request_body

    def _load_portfolio(self) -> str:
        """Loads and returns the portfolio as a string."""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            return f.read()
