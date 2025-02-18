"""
This module defines strategy for excel exporting.
"""


import os
import click
from typing import Dict, Any, List
import pandas as pd
from .export_strategy import ExportStrategy


class ExcelExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to Excel."""

    def export(self, date: str, version: bool, data: List[Dict[str, Any]], output_path: str) -> None:
        """Concrete implementation for exporting into excel."""
        if data:
            version_path = "LIVE" if version else "SOD"

            out_path = f"{date}_{version_path}_{self.type}.xlsx"
            file_path = os.path.join(output_path, out_path)
            df = pd.DataFrame(data)
            df.to_excel(file_path, sheet_name="products", index=False)
        else:
            click.echo("No data found.")
