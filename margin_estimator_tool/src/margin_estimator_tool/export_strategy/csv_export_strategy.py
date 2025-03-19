"""
This module defines strategy for CSV exporting.
"""

import os
import csv
from typing import Dict, Any, List
from .export_strategy import ExportStrategy


class CSVExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to CSV."""

    def export(
        self, date: str, version: bool, data: List[Dict[str, Any]], output_path: str
    ) -> bool:
        """
        Concrete implementation for exporting into CSV.

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

        version_path = "LIVE" if version else "SOD"
        out_path = f"{date}_{version_path}_{self.type}.csv"
        file_path = os.path.join(output_path, out_path)
        keys = data[0].keys()

        with open(file_path, "w", newline="") as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

        return True
