from .export_strategy import ExportStrategy
from typing import Dict, Any, List
import pandas as pd
import openpyxl


class ExcelExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to Excel."""

    def export(self, date: str, version: bool, products: List[Dict[str, Any]], output_path: str):
        version_path = "LIVE" if version else "SOD"

        out_path = f'{output_path}/{date}_{version_path}_products.xlsx'
        df = pd.DataFrame(products)
        df.to_excel(out_path, sheet_name='products', index=False)
