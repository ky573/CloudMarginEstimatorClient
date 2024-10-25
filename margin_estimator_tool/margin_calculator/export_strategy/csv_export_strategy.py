import csv
from .export_strategy import ExportStrategy


class CSVExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to CSV."""

    def export(self, products, output_path):
        pass
