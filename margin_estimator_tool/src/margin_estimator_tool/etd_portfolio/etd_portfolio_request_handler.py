"""
This module contains logic for retrieving information about products from
endpoint and then outputting them in desired form.
"""


import csv
from typing import Dict, Any
import os
import click
from margin_estimator_tool.src.margin_estimator_tool.core.data_exporter import DataExporter
from margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base import RequestHandler
from margin_estimator_tool.src.margin_estimator_tool.core.utils import setup_estimator_request_body

# dodelat tridu na mapping do POrtfolioInner


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
        self.export_dir = export_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def process_and_provide_output(self) -> None:
        """Processes the data from /estimator and exports it according to the specified format."""
        if not self._validate_header():
            return

        portfolio = self.send_request()
        DataExporter.export(portfolio,
                            "Portfolio",
                            self.export_dir,
                            self.to_excel,
                            self.to_json,
                            str(self.business_date),
                            self.version)

    def send_request(self) -> Dict[str, Any]:
        """Sends a POST request to /estimator endpoint with provided portfolio."""
        request_body = setup_estimator_request_body(self.business_date,
                                                    self._load_portfolio(),
                                                    self.version,
                                                    self.timestamp)
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
            with open(self.csv_file, mode='r', newline='', encoding="utf-8") as csvfile:
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

    def _load_portfolio(self) -> str:
        """Loads and returns the portfolio as a string."""
        with open(self.csv_file, 'r', encoding="utf-8") as f:
            return f.read()
