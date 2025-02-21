"""
This module contains logic for retrieving information about products from
endpoint and then outputting them in desired form.
"""


import csv
import json
from typing import Dict, Any, Optional
import os
import click
from margin_estimator_tool.src.margin_estimator_tool.core.data_exporter import DataExporter
from margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base import RequestHandler
from margin_estimator_tool.src.margin_estimator_tool.core.utils import (setup_estimator_request_gui,
                                                                        setup_estimator_request_inner,
                                                                        setup_request_body)


class EtdPortfolioRequestHandler(RequestHandler):
    """Handler for sending requests to the /estimator endpoint and exporting data."""

    GUI_HEADER = "Product ID,Contract Date,Call Put Flag,Exercise Price,Version Number,Net LS Balance"
    INNER_HEADER = "call_put_flag,component_margin,component_margin_currency,contract_date,exercise_price,exercise_style,iid,instrument_type,line_no,liquidation_group,liquidation_group_split,maturity,net_ls_balance,premium_margin,premium_margin_currency,product_id,version_number"

    def __init__(self,
                 csv_file: str,
                 date: Optional[str] = None,
                 version: Optional[str] = None,
                 timestamp: Optional[int] = None,
                 to_excel: Optional[bool] = False,
                 to_json: Optional[bool] = False,
                 export_dir: Optional[str] = None,
                 ) -> None:
        """
        Initializes the EtdPortfolioRequestHandler instance.

        Args:
            csv_file: path to csv file containing portfolio
            date: desired business date, decided by method get_business_date
            version: desired version, defaults to SOD
            timestamp: timestamp for request, defaults to 0
            to_excel: whether to export to excel
            to_json: whether to export to json
            export_dir: directory where data will be exported, defaults to project's root
        """
        super().__init__()
        self.csv_file = csv_file
        self.business_date = self._get_business_date(date, version)
        self.version = version == "LIVE"
        self.timestamp = timestamp if timestamp is not None else 0
        self.to_excel = to_excel
        self.to_json = to_json
        self.export_dir = export_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.gui_header = False
        self.inner_header = False

    def process_and_provide_output(self) -> None:
        """
        Processes the data from /estimator and exports it according to the specified format.
        If the header is not validated properly, it returns immediately.
        """
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
        """
        Sends a POST request to /estimator endpoint with provided portfolio.

        Returns:
            response: Response returned from the endpoint containing data about portoflio.
                      If an error is encountered during the request, it returns an empty dictionary.
        """
        if self.gui_header:
            estimator_request_body = setup_estimator_request_gui(self.business_date,
                                                                 self.csv_file,
                                                                 self.version,
                                                                 self.timestamp)
        else:
            estimator_request_body = setup_estimator_request_inner(self.business_date,
                                                                   self.csv_file,
                                                                   self.version,
                                                                   self.timestamp)

        try:
            response = self.api.estimator_post(body=estimator_request_body.to_dict())
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
                if headers_str == self.GUI_HEADER:
                    self.gui_header = True
                elif headers_str == self.INNER_HEADER:
                    self.inner_header = True

                if not self.gui_header and not self.inner_header:
                    raise ValueError(f"Headers mismatch. Expected: either '{self.GUI_HEADER}' "
                                     f"or '{self.INNER_HEADER}', Found: '{headers_str}'.")

            click.echo("Headers validated successfully.")
            return True
        except (ValueError, FileNotFoundError) as e:
            click.echo(f"Error validating CSV headers: {e}")
            return False

    def _load_portfolio(self) -> str:
        """Loads and returns the portfolio as a string."""
        with open(self.csv_file, 'r', encoding="utf-8") as f:
            return f.read()
