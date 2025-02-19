"""
This module defines an interface for export strategy, so that modules can
use it for exporting data to various formats.
"""


from abc import ABC, abstractmethod
from typing import Dict, Any, List


class ExportStrategy(ABC):
    """Interface for exporting product data."""

    def __init__(self, type: str):
        self.type = type

    @abstractmethod
    def export(self,
               date: str,
               version: bool,
               data: List[Dict[str, Any]] | Dict[str, Any],
               output_path: str
               ) -> bool:
        """Abstract method to be implemented by subclasses."""
