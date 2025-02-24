"""
This module contains logic for retrieving information about products from
endpoint and then outputting them in desired form.
"""


from typing import Dict, Any, Optional
import os
from margin_estimator_tool.src.margin_estimator_tool.core.data_exporter import DataExporter
from margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base import RequestHandler
from margin_estimator_tool.src.margin_estimator_tool.estimator.estimator_request_handler_base import \
    EstimatorRequestHandlerBase


class EtdPortfolioRequestHandler(RequestHandler, EstimatorRequestHandlerBase):
    """Handler for sending requests to the /estimator endpoint and exporting data."""

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
        RequestHandler.__init__(self)
        EstimatorRequestHandlerBase.__init__(self)
        self.csv_file = csv_file
        self.business_date = self._get_business_date(date, version)
        self.version = version == "LIVE"
        self.timestamp = timestamp if timestamp is not None else 0
        self.to_excel = to_excel
        self.to_json = to_json
        self.export_dir = export_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def process_and_provide_output(self) -> None:
        """
        Processes the data from /estimator and exports it according to the specified format.
        If the header is not validated properly, it returns immediately.
        """
        if not self._validate_header(self.csv_file):
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
        estimator_request_body = self.create_correct_request_body(self.business_date,
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
