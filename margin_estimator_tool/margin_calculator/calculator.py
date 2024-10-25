"""
This module contains the MarginCalculator class which is responsible for calculating the margin,
extracting data from API responses, running POST requests in parallel, and saving the results.
It uses helper classes for handling requests to the API, exporting the initial margin graph,
and exporting data to an Excel file. It also uses utility functions to determine business days.
"""

from typing import List, Dict, Any
import json
from datetime import datetime
import click
from .estimator_request_handler import EstimatorRequestHandler
from .graph_exporter import GraphExporter
from .excel_exporter import ExcelExporter
from .utils import collect_business_days


class MarginCalculator:
    """Class to handle the margin calculation and exporting of results."""
    INITIAL_MARGIN_INDEX = 0  # Index of the initial margin in the portfolio margin list

    def __init__(self, portfolio: str):
        self.portfolio = portfolio
        self.handler = EstimatorRequestHandler()
        self.initial_margins: List[float] = []
        self.dates: List[int] = []
        self.margin_details: List[Dict[str, Any]] = []

    def _extract_data(self, data: Dict[str, Any]) -> None:
        """Extracts and aggregates initial margin data from the API response."""
        business_date = int(data['business_date'])
        self.dates.append(business_date)
        initial_margin = data['portfolio_margin'][self.INITIAL_MARGIN_INDEX]['initial_margin']
        self.initial_margins.append(float(initial_margin))

        # Store margin details for export
        self.margin_details.append({
            "business_date": business_date,
            "portfolio_margin": data.get('portfolio_margin'),
            "drilldowns": data.get('drilldowns')
        })

    def _run_post_requests(self, business_days: List[int]) -> None:
        """Runs POST requests to estimator endpoint."""
        for business_day in business_days:
            data = self.handler.send_request(business_day, self.portfolio)
            print(json.dumps(data, indent=4))
            if data:
                self._extract_data(data)
            else:
                click.echo("Error with one of the requests.")

    def _save_results(self, export_dir: str) -> None:
        """Saves the graph and Excel report."""
        self._save_excel(export_dir)
        self._save_graph(export_dir)

    def _save_excel(self, export_dir: str) -> None:
        """Saves the Excel report."""
        excel_exporter = ExcelExporter(self.margin_details, export_dir)
        excel_exporter.export_to_excel()

    def _save_graph(self, export_dir: str) -> None:
        """Saves the graph."""
        graph_exporter = GraphExporter(self.dates, self.initial_margins, export_dir)
        graph_exporter.save_graph()

    def run(self, date_from: str, date_to: str, export_dir: str) -> None:
        """Main function to run the margin calculation."""
        start_date = datetime.strptime(date_from, "%Y%m%d")
        end_date = datetime.strptime(date_to, "%Y%m%d")

        business_days = collect_business_days(start_date, end_date)
        self._run_post_requests(business_days)
        self._save_results(export_dir)
