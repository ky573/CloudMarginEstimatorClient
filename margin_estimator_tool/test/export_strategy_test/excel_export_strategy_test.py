"""Test suite for the ExcelExportStrategy class."""

import os
from unittest.mock import patch
from margin_estimator_tool.export_strategy.excel_export_strategy import (
    ExcelExportStrategy,
)


class TestExcelExportStrategy:
    """Test cases for the ExcelExportStrategy class."""

    def setup_method(self):
        """Setup test data before each test."""
        self.strategy = ExcelExportStrategy("products")
        self.date = "20250318"
        self.version = True
        self.output_path = "test_dir"
        self.data = [
            {"key1": "value1", "key2": "value2"},
            {"key1": "value3", "key2": "value4"},
        ]
        self.expected_filename = os.path.join(
            self.output_path, f"{self.date}_LIVE_products.xlsx"
        )

    def test_export_success(self):
        """Tests exporting data successfully to an Excel file."""
        with patch("pandas.DataFrame.to_excel") as mock_to_excel:
            result = self.strategy.export(
                self.date, self.version, self.data, self.output_path
            )

            assert result is True
            mock_to_excel.assert_called_once_with(
                self.expected_filename, sheet_name="products", index=False
            )

    def test_export_no_data(self):
        """Tests exporting when data is empty, expecting False."""
        with patch("pandas.DataFrame.to_excel") as mock_to_excel:
            result = self.strategy.export(self.date, self.version, [], self.output_path)

            assert result is False
            mock_to_excel.assert_not_called()
