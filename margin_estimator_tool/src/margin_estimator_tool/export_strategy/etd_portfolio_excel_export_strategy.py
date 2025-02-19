"""
This module defines strategy for etd portfolio exporting into excel.
"""


import os
import click
import pandas as pd
from typing import Dict, Any, List
from .export_strategy import ExportStrategy
from margin_estimator_tool.src.margin_estimator_tool.core.utils import flatten_dict


class EtdPortfolioExcelExportStrategy(ExportStrategy):
    """Concrete strategy for exporting portfolio data to Excel."""

    def export(self, date: str, version: bool, portfolio_data: Dict[str, Any], output_path: str) -> bool:
        """
        Exports portfolio data into an Excel file with two subsheets.

        Args:
            date: date to be included in file name
            version: version to be included in file name
            portfolio_data: data from response to be exported
            output_path: directory where data will be exported

        Returns:
            True if there were any data to export, false otherwise
        """
        version_path = "LIVE" if version else "SOD"
        file_path = os.path.join(output_path, f"{date}_{version_path}_portfolio.xlsx")

        portfolio_margin = portfolio_data.get("portfolio_margin", [])
        drilldowns = portfolio_data.get("drilldowns", [])

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            margin_success = self.export_margins(portfolio_margin, writer)
            drilldowns_success = self.export_drilldowns(drilldowns, writer)

        return margin_success or drilldowns_success

    @staticmethod
    def export_drilldowns(drilldowns: List[Dict[str, Any]], writer: pd.ExcelWriter) -> bool:
        if drilldowns:
            pd.DataFrame(drilldowns).to_excel(writer, sheet_name="Drilldowns", index=False)
            drilldowns_success = True
        else:
            click.echo("No drilldowns found in response.")
            drilldowns_success = False
        return drilldowns_success

    @staticmethod
    def export_margins(portfolio_margin: List[Dict[str, Any]], writer: pd.ExcelWriter):
        if portfolio_margin:
            pd.DataFrame([flatten_dict(entry) for entry in portfolio_margin]).to_excel(writer,
                                                                                       sheet_name="Portfolio Margin",
                                                                                       index=False)
            margin_success = True
        else:
            click.echo("No portfolio margins found in response.")
            margin_success = False
        return margin_success
