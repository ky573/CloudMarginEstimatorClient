import csv
from .export_strategy import ExportStrategy
from typing import Dict, Any, List
import os


class CSVExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to CSV."""

    def export(self, date: str, version: bool, products: List[Dict[str, Any]], output_path: str):
        version_path = "LIVE" if version else "SOD"

        out_path = f'{date}_{version_path}_products.csv'
        file_path = os.path.join(output_path, out_path)
        keys = products[0].keys()
        with open(file_path, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(products)
