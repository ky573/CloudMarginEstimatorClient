from abc import ABC, abstractmethod
from typing import Dict, Any, List


class ExportStrategy(ABC):
    """Interface for exporting product data."""

    def __init__(self, type: str):
        self.type = type

    @abstractmethod
    def export(self, date: str, version: bool, products: List[Dict[str, Any]], output_path: str) -> None:
        pass
