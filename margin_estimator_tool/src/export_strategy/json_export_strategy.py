"""This module defines strategy for JSON exporting."""

import os
import json
from typing import Dict, Any, List
from export_strategy.export_strategy import ExportStrategy


class JSONExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to JSON."""

    def export(
        self, date: str, version: bool, data: List[Dict[str, Any]], output_path: str
    ) -> bool:
        """
        Concrete implementation for exporting into JSON.

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
        out_path = f"{date}_{version_path}_{self._type}.json"
        file_path = os.path.join(output_path, out_path)
        with open(file_path, "w") as output_file:
            json.dump(data, output_file, indent=4)

        return True
