"""
This module defines strategy for JSON exporting.
"""


import os
import json
from typing import Dict, Any, List
from .export_strategy import ExportStrategy


class JSONExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to JSON."""

    def export(self, date: str, version: bool, products: List[Dict[str, Any]], output_path: str):
        """Concrete implementation for exporting into JSON."""
        version_path = "LIVE" if version else "SOD"

        out_path = f'{date}_{version_path}_{self.type}.json'
        file_path = os.path.join(output_path, out_path)
        with open(file_path, 'w') as output_file:
            json.dump(products, output_file, indent=4)
