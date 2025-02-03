"""
This module defines context for exporting the data.
"""

from typing import Dict, Any, List


class ExportContext:
    """Context for using the export strategy."""

    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy) -> None:
        """Sets the strategy for exporting."""
        self.strategy = strategy

    def export_data(self,
                    date: str,
                    version: bool,
                    data: List[Dict[str, Any]] | Dict[str, Any],
                    output_path: str
                    ) -> None:
        """Exports the data in desired format."""
        if self.strategy:
            self.strategy.export(date, version, data, output_path)
        else:
            print("No export strategy defined.")
