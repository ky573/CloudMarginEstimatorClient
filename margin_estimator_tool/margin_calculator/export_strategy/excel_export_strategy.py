from .export_strategy import ExportStrategy


class ExcelExportStrategy(ExportStrategy):
    """Concrete strategy for exporting to Excel."""

    def export(self, products, output_path):
        pass
