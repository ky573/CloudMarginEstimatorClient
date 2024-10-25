from abc import ABC, abstractmethod
from typing import Dict, Any


class ExportStrategy(ABC):
    """Interface for exporting product data."""

    @abstractmethod
    def export(self, products, output_path: str) -> None:
        pass
