"""
This module defines an interface for export strategy, so that modules can
use it for exporting data to various formats.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class ExportStrategy(ABC):
    """Interface for exporting product data."""

    def __init__(self, type: str) -> None:
        """
        Initializes ExportStrategy instance.

        Args:
            type: type of the strategy used
        """
        self._type = type

    @abstractmethod
    def export(
        self,
        date: str,
        version: bool,
        data: List[Dict[str, Any]] | Dict[str, Any],
        output_path: str,
    ) -> bool:
        """
        Abstract method for exporting to be implemented by subclasses.

        Args:
            date: date to be included in file name
            version: version to be included in file name
            data: data from response to be exported
            output_path: directory where data will be exported

        Returns:
            True if there were any data to export, false otherwise
        """
