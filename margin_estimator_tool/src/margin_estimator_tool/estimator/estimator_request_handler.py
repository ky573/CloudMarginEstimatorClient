"""
This module is responsible for sending the request to estimator endpoint,
fetching the results and exporting them.
"""


from typing import Dict, Any, List
from datetime import datetime
import click
from margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base import RequestHandler
from margin_estimator_tool.src.margin_estimator_tool.estimator.extractor import Extractor
from margin_estimator_tool.src.margin_estimator_tool.estimator.portfolio_loader import PortfolioLoader
from margin_estimator_tool.src.margin_estimator_tool.estimator.graph_exporter import GraphExporter
from margin_estimator_tool.src.margin_estimator_tool.estimator.excel_exporter import ExcelExporter
from margin_estimator_tool.src.margin_estimator_tool.core.utils import (collect_business_days,
                                                                        setup_estimator_request_gui)


class EstimatorRequestHandler(RequestHandler):
    """Handler for sending requests to the /estimator endpoint."""

    def __init__(self, date_from: str, date_to: str, export_dir: str):
        super().__init__()
        self.date_from = date_from
        self.date_to = date_to
        self.export_dir = export_dir
        self.portfolio = PortfolioLoader().load_portfolio()
        self.extractor = Extractor()

    def process_and_provide_output(self) -> None:
        """Main method to process and export margin data."""
        business_days = self._collect_business_days()
        margin_data = self._fetch_margin_data(business_days)

        if margin_data:
            self._export_results(margin_data)
            click.echo(f"Margins exported to {self.export_dir}")

    def _fetch_margin_data(self, business_days: List[int]) -> List[Dict[str, Any]]:
        """Fetches and aggregates margin data for each business day."""
        margin_data = []
        for business_day in business_days:
            data = self.send_request(business_day, self.portfolio)
            if data:
                self.extractor.extract_data(data)
                margin_data.append(data)
        return margin_data

    def send_request(self, business_date: int, portfolio: str) -> Dict[str, Any]:
        """Sends a POST request to the /estimator endpoint with the specified data."""
        request_body = setup_estimator_request_gui(business_date, portfolio)
        try:
            response = self.api.estimator_post(body=request_body.to_dict())
            self._check_for_error_in_response(response)
            return response
        except Exception as e:
            self._handle_request_error(e)
        return {}

    def _collect_business_days(self) -> List[int]:
        """Collects the list of business days for the calculation period."""
        start_date = datetime.strptime(self.date_from, "%Y%m%d")
        end_date = datetime.strptime(self.date_to, "%Y%m%d")
        return collect_business_days(start_date, end_date)

    def _export_results(self, margin_data: List[Dict[str, Any]]) -> None:
        """Exports margin details to Excel and graph formats."""
        excel_exporter = ExcelExporter(margin_data, self.export_dir)
        excel_exporter.export_to_excel()

        graph_exporter = GraphExporter(
            self.extractor.dates, self.extractor.initial_margins, self.export_dir
        )
        graph_exporter.save_graph()
