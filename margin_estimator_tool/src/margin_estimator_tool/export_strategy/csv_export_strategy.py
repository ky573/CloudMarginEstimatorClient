"""
This module defines strategy for CSV exporting.
"""


import os
import csv
from typing import Dict, Any, List
from .export_strategy import ExportStrategy


class CSVExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to CSV."""

    def export(self, date: str, version: bool, data: List[Dict[str, Any]], output_path: str) -> bool:
        """Concrete implementation for exporting into CSV."""
        if data:
            version_path = "LIVE" if version else "SOD"
            out_path = f"{date}_{version_path}_{self.type}.csv"
            file_path = os.path.join(output_path, out_path)
            keys = data[0].keys()
            with open(file_path, 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)

            return True
        else:
            return False
