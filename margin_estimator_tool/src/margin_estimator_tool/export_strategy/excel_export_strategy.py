"""This module defines strategy for Excel exporting."""

import os
from typing import Dict, Any, List
import pandas as pd
from .export_strategy import ExportStrategy


class ExcelExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to Excel."""

    def export(
        self, date: str, version: bool, data: List[Dict[str, Any]], output_path: str
    ) -> bool:
        """
        Concrete implementation for exporting into Excel.

        Args:
            date: date to be included in file name
            version: version to be included in file name
            data: data from response to be exported
            output_path: directory where data will be exported

        Returns:
            True if there were any data to export, false otherwise
        """
        if not data:
            return False

        version_path = "LIVE" if version else "EOD"
        out_path = f"{date}_{version_path}_{self._type}.xlsx"
        file_path = os.path.join(output_path, out_path)
        df = pd.DataFrame(data)
        df.to_excel(file_path, sheet_name="products", index=False)

        return True
