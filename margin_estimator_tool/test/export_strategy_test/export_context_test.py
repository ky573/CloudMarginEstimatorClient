"""Test suite for the ExportContext class."""

from unittest.mock import MagicMock
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.export_strategy import (
    ExportStrategy,
)
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.export_context import (
    ExportContext,
)


class TestExportContext:
    """Test cases for the ExportContext class."""

    def setup_method(self):
        """Setup test data before each test."""
        self.mock_strategy = MagicMock(spec=ExportStrategy)
        self.context = ExportContext()

    def test_initialization(self):
        """Tests that the context is initialized without a strategy."""
        assert self.context.strategy is None

    def test_set_strategy(self):
        """Tests setting an export strategy."""
        self.context.set_strategy(self.mock_strategy)
        assert self.context.strategy == self.mock_strategy

    def test_export_data_with_strategy(self):
        """Tests exporting data with a valid strategy."""
        self.context.set_strategy(self.mock_strategy)
        self.mock_strategy.export.return_value = True

        result = self.context.export_data(
            "20250318", True, [{"key": "value"}], "test_dir"
        )

        self.mock_strategy.export.assert_called_once_with(
            "20250318", True, [{"key": "value"}], "test_dir"
        )
        assert result is True

    def test_export_data_without_strategy(self, capsys):
        """Tests exporting data without setting a strategy (should print a message and return False)."""
        result = self.context.export_data(
            "20250318", True, [{"key": "value"}], "test_dir"
        )

        captured = capsys.readouterr()
        assert "No export strategy defined." in captured.out
        assert result is False
