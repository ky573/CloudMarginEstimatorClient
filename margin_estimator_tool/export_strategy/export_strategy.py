from abc import ABC, abstractmethod
from typing import Dict, Any, List


class ExportStrategy(ABC):
    """Interface for exporting product data."""

    @abstractmethod
    def export(self, date: str, version: bool, products: List[Dict[str, Any]], output_path: str) -> None:
        pass
