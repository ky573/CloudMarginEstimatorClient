"""
This module defines context for exporting the data.
"""


from typing import Dict, Any, List

from margin_estimator_tool.src.margin_estimator_tool.export_strategy.export_strategy import ExportStrategy


class ExportContext:
    """Context for using the export strategy."""

    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy: ExportStrategy) -> None:
        """Sets the strategy for exporting."""
        self.strategy = strategy

    def export_data(self,
                    date: str,
                    version: bool,
                    data: List[Dict[str, Any]] | Dict[str, Any],
                    output_path: str
                    ) -> bool:
        """Exports the data in desired format."""
        if self.strategy:
            return self.strategy.export(date, version, data, output_path)
        else:
            print("No export strategy defined.")
