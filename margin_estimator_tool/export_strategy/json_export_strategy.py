import json
from .export_strategy import ExportStrategy
from typing import Dict, Any, List
import os


class JSONExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to JSON."""

    def export(self, date: str, version: bool, products: List[Dict[str, Any]], output_path: str):
        version_path = "LIVE" if version else "SOD"

        out_path = f'{date}_{version_path}_{self.type}.json'
        file_path = os.path.join(output_path, out_path)
        with open(file_path, 'w') as output_file:
            json.dump(products, output_file, indent=4)
