from .export_strategy import ExportStrategy
from typing import Dict, Any, List
import pandas as pd
import os


class ExcelExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to Excel."""

    def export(self, date: str, version: bool, products: List[Dict[str, Any]], output_path: str):
        version_path = "LIVE" if version else "SOD"

        out_path = f'{date}_{version_path}_products.xlsx'
        file_path = os.path.join(output_path, out_path)
        df = pd.DataFrame(products)
        df.to_excel(file_path, sheet_name='products', index=False)
