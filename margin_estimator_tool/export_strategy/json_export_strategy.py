import json
from .export_strategy import ExportStrategy
from typing import Dict, Any, List


class JSONExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to JSON."""

    def export(self, date: str, version: bool, products: List[Dict[str, Any]], output_path: str):
        version_path = "LIVE" if version else "SOD"

        out_path = f'{output_path}/{date}_{version_path}_products.json'
        with open(out_path, 'w') as output_file:
            json.dump(products, output_file, indent=4)
