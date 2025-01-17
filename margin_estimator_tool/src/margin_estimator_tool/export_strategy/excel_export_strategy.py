"""
This module defines strategy for excel exporting.
"""


import os
from typing import Dict, Any, List
import pandas as pd
from .export_strategy import ExportStrategy


class ExcelExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to Excel."""

    def export(self, date: str, version: bool, products: List[Dict[str, Any]], output_path: str):
        """Concrete implementation for exporting into excel."""
        version_path = "LIVE" if version else "SOD"

        out_path = f'{date}_{version_path}_{self.type}.xlsx'
        file_path = os.path.join(output_path, out_path)
        df = pd.DataFrame(products)
        df.to_excel(file_path, sheet_name='products', index=False)
