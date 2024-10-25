class ExportContext:
    """Context for using the export strategy."""

    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def export_data(self, products, output_path):
        if self.strategy:
            self.strategy.export(products, output_path)
        else:
            print("No export strategy defined.")
