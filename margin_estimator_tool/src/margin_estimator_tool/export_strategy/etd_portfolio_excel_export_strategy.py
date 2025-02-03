"""
This module defines strategy for etd portfolio exporting into excel.
"""


import os
import pandas as pd
from typing import Dict, Any
from .export_strategy import ExportStrategy
from margin_estimator_tool.src.margin_estimator_tool.core.utils import flatten_dict

class EtdPortfolioExcelExportStrategy(ExportStrategy):
    """Concrete strategy for exporting portfolio data to Excel."""

    def export(self, date: str, version: bool, portfolio_data: Dict[str, Any], output_path: str) -> None:
        """Exports portfolio data into an Excel file with two subsheets."""
        version_path = "LIVE" if version else "SOD"
        file_path = os.path.join(output_path, f"{date}_{version_path}_portfolio.xlsx")

        portfolio_margin = portfolio_data.get("portfolio_margin", [])
        drilldowns = portfolio_data.get("drilldowns", [])

        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            if portfolio_margin:
                pd.DataFrame([flatten_dict(entry) for entry in portfolio_margin]).to_excel(writer, sheet_name='Portfolio Margin', index=False)
            if drilldowns:
                pd.DataFrame(drilldowns).to_excel(writer, sheet_name='Drilldowns', index=False)
