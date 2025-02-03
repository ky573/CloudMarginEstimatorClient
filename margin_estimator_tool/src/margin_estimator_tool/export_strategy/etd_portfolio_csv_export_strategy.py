"""
This module defines strategy for etd portfolio exporting into csv.
"""


import os
import csv
from typing import Dict, Any
from .export_strategy import ExportStrategy
from margin_estimator_tool.src.margin_estimator_tool.core.utils import flatten_dict


class EtdPortfolioCSVExportStrategy(ExportStrategy):
    """Concrete strategy for exporting portfolio data to CSV."""

    def export(self, date: str, version: bool, portfolio_data: Dict[str, Any], output_path: str) -> None:
        """Exports portfolio data into separate CSV files for portfolio_margin and drilldowns."""
        version_path = "LIVE" if version else "SOD"

        self._export_portfolio_margin(date, version_path, portfolio_data, output_path)
        self._export_drilldowns(date, version_path, portfolio_data, output_path)

    def _export_portfolio_margin(self, date: str, version_path: str, portfolio_data: Dict[str, Any], output_path: str) -> None:
        """Exports portfolio margins into designated csv file."""
        portfolio_margin = portfolio_data.get("portfolio_margin", [])
        portfolio_margin_path = os.path.join(output_path, f"{date}_{version_path}_portfolio_portfolio_margin.csv")

        flattened_data = [flatten_dict(entry) for entry in portfolio_margin]
        with open(portfolio_margin_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=flattened_data[0].keys())
            writer.writeheader()
            writer.writerows(flattened_data)

    def _export_drilldowns(self, date: str, version_path: str, portfolio_data: Dict[str, Any], output_path: str) -> None:
        """Exports drilldowns into designated csv file."""
        drilldowns = portfolio_data.get("drilldowns", [])
        drilldowns_path = os.path.join(output_path, f"{date}_{version_path}_portfolio_drilldowns.csv")

        with open(drilldowns_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=drilldowns[0].keys())
            writer.writeheader()
            writer.writerows(drilldowns)
