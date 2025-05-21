"""
This module contains logic for retrieving information about etd portfolio from
endpoint and then outputting it in desired format.
"""

import json
from typing import Dict, Any, Optional
import os
import click
from core.data_exporter import DataExporter
from core.request_handler_base import RequestHandler
from estimator.estimator_request_builder import EstimatorRequestBuilder
from estimator.portfolio_header_validator import HeaderValidator


class EtdPortfolioRequestHandler(RequestHandler):
    """Handler for sending requests to the /estimator endpoint and exporting data."""

    def __init__(
        self,
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
            version: desired version, defaults to EOD
            timestamp: timestamp for request, defaults to 0
            to_excel: whether to export to excel
            to_json: whether to export to json
            export_dir: directory where data will be exported, defaults to project's root
        """
        super().__init__()
        self._header_validator = HeaderValidator()
        self._request_builder = EstimatorRequestBuilder(self._header_validator)
        self._csv_file = csv_file
        self._business_date = self._get_business_date(date, version)
        self._version = version == "LIVE"
        self._timestamp = timestamp if timestamp is not None else 0
        self._to_excel = to_excel
        self._to_json = to_json
        self._export_dir = export_dir or os.getcwd()

    def process_and_provide_output(self) -> None:
        """
        Processes the data from /estimator and exports it according to the specified format.
        If the header is not validated properly, it returns immediately.
        """
        if not self._header_validator.validate_headers(self._csv_file):
            click.echo("Failed to validate CSV portfolio file. Process aborted.")
            return

        portfolio = self.send_request()
        DataExporter.export(
            portfolio,
            "Portfolio",
            self._export_dir,
            self._to_excel,
            self._to_json,
            str(self._business_date),
            self._version,
        )

    def send_request(self) -> Dict[str, Any]:
        """
        Sends a POST request to /estimator endpoint with provided portfolio.

        Returns:
            response: Response returned from the endpoint containing data about portoflio.
                      If an error is encountered during the request, it returns an empty dictionary.
        """
        estimator_request_body = self._request_builder.build_request(
            self._business_date, self._csv_file, self._version, self._timestamp
        )
        try:
            response = self._api.estimator_post(body=estimator_request_body.to_dict())
            self._check_for_error_in_response(response)
            return response
        except Exception as e:
            self._handle_request_error(e)
        return {}
