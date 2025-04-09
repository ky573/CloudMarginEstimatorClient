"""
This module defines strategy for etd portfolio exporting into csv.
"""

import os
import csv
from typing import Dict, Any
import click
from margin_estimator_tool.core.utils import flatten_dict
from .export_strategy import ExportStrategy


class EtdPortfolioCSVExportStrategy(ExportStrategy):
    """Concrete strategy for exporting portfolio data to CSV."""

    def export(
        self, date: str, version: bool, portfolio_data: Dict[str, Any], output_path: str
    ) -> bool:
        """
        Exports portfolio data into separate CSV files for portfolio_margin and drilldowns.

        Args:
            date: date to be included in file name
            version: version to be included in file name
            portfolio_data: data from response to be exported
            output_path: directory where data will be exported

        Returns:
            True if there were any data to export, false otherwise
        """
        version_path = "LIVE" if version else "SOD"

        margins_success = self._export_portfolio_margin(
            date, version_path, portfolio_data, output_path
        )
        drilldowns_success = self._export_drilldowns(
            date, version_path, portfolio_data, output_path
        )

        return margins_success or drilldowns_success

    @staticmethod
    def _export_portfolio_margin(
        date: str, version_path: str, portfolio_data: Dict[str, Any], output_path: str
    ) -> bool:
        """Exports portfolio margins into designated csv file."""
        portfolio_margin = portfolio_data.get("portfolio_margin", [])
        portfolio_margin_path = os.path.join(
            output_path, f"{date}_{version_path}_portfolio_margin.csv"
        )

        flattened_data = [flatten_dict(entry) for entry in portfolio_margin]

        if not flattened_data:
            click.echo("No portfolio margins found in response.")
            return False

        with open(portfolio_margin_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=flattened_data[0].keys())
            writer.writeheader()
            writer.writerows(flattened_data)

        return True

    @staticmethod
    def _export_drilldowns(
        date: str, version_path: str, portfolio_data: Dict[str, Any], output_path: str
    ) -> bool:
        """Exports drilldowns into designated csv file."""
        drilldowns = portfolio_data.get("drilldowns", [])
        drilldowns_path = os.path.join(
            output_path, f"{date}_{version_path}_portfolio_drilldowns.csv"
        )

        if not drilldowns:
            click.echo("No drilldowns found in response.")
            return False

        with open(drilldowns_path, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=drilldowns[0].keys())
            writer.writeheader()
            writer.writerows(drilldowns)

        return True
