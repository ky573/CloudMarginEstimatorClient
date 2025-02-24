"""
This module is responsible for sending the request to estimator endpoint,
fetching the results and exporting them.
"""


from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import click
from margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base import RequestHandler
from margin_estimator_tool.src.margin_estimator_tool.estimator.estimator_request_handler_base import \
    EstimatorRequestHandlerBase
from margin_estimator_tool.src.margin_estimator_tool.estimator.margin_calculator.extractor import Extractor
from margin_estimator_tool.src.margin_estimator_tool.estimator.margin_calculator.graph_exporter import GraphExporter
from margin_estimator_tool.src.margin_estimator_tool.estimator.margin_calculator.excel_exporter import ExcelExporter


class MarginCalculatorRequestHandler(RequestHandler, EstimatorRequestHandlerBase):
    """Handler for sending requests to the /estimator endpoint."""

    def __init__(self,
                 csv_file: str,
                 version: Optional[str],
                 timestamp: Optional[int],
                 date_from: str,
                 date_to: str,
                 export_dir: str
                 ) -> None:
        RequestHandler.__init__(self)
        EstimatorRequestHandlerBase.__init__(self)
        self.csv_file = csv_file
        self.version = version == "LIVE"
        self.timestamp = timestamp if timestamp is not None else 0
        self.date_from = date_from
        self.date_to = date_to
        self.export_dir = export_dir
        self.extractor = Extractor()

    def process_and_provide_output(self) -> None:
        """Main method to process and export margin data."""
        if not self._validate_header(self.csv_file):
            return

        business_days = self._collect_business_days()
        margin_data = self._fetch_margin_data(business_days)

        if margin_data:
            self._export_results(margin_data)
            click.echo(f"Margins exported to {self.export_dir}")

    def send_request(self, business_date: int) -> Dict[str, Any]:
        """Sends a POST request to the /estimator endpoint with the specified data."""
        estimator_request_body = self.create_correct_request_body(business_date,
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

    def _fetch_margin_data(self, business_days: List[int]) -> List[Dict[str, Any]]:
        """Fetches and aggregates margin data for each business day."""
        margin_data = []
        for business_day in business_days:
            data = self.send_request(business_day)
            if data:
                self.extractor.extract_data(data)
                margin_data.append(data)
        return margin_data

    def _collect_business_days(self) -> List[int]:
        """Collects the list of business days for the calculation period."""
        start_date = datetime.strptime(self.date_from, "%Y%m%d")
        end_date = datetime.strptime(self.date_to, "%Y%m%d")

        current_date = start_date
        business_days: List[int] = []

        while current_date <= end_date:
            if self._is_business_day(current_date):
                business_days.append(int(current_date.strftime("%Y%m%d")))
            current_date += timedelta(days=1)

        return business_days

    def _export_results(self, margin_data: List[Dict[str, Any]]) -> None:
        """Exports margin details to Excel and graph formats."""
        excel_exporter = ExcelExporter(margin_data, self.export_dir)
        excel_exporter.export_to_excel()

        graph_exporter = GraphExporter(
            self.extractor.dates, self.extractor.initial_margins, self.export_dir
        )
        graph_exporter.save_graph()
