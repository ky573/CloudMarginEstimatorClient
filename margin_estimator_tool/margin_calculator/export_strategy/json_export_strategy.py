import json
from .export_strategy import ExportStrategy


class JSONExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to JSON."""

    def export(self, products, output_path):
        pass
