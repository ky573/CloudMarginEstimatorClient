"""Test suite for MarginCalculatorExcelExportStrategy class"""

import os
from unittest.mock import patch, MagicMock
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.margin_calculator_excel_export_strategy import (
    MarginCalculatorExcelExportStrategy,
)


class TestMarginCalculatorExcelExportStrategy:
    """Test cases for the MarginCalculatorExcelExportStrategy class."""

    def setup_method(self):
        """Setup test data before each test."""
        self.strategy = MarginCalculatorExcelExportStrategy("margins")
        self.date = "20250318"
        self.version = True
        self.output_path = "test_dir"
        self.data = [
            {
                "business_date": "20250318",
                "portfolio_margin": [
                    {"key1": "value1", "key2": "value2"},
                    {"key1": "value3", "key2": "value4"},
                ],
                "drilldowns": [
                    {"drill_key1": "drill_value1", "drill_key2": "drill_value2"}
                ],
            }
        ]
        self.expected_filename = os.path.join(
            self.output_path, f"{self.date}_LIVE_margin.xlsx"
        )

    def test_export_success(self):
        """Tests exporting margin data successfully to an Excel file."""
        with patch("openpyxl.Workbook.save") as mock_save:
            mock_save.return_value = None  # Prevents actual file writing

            result = self.strategy.export(self.date, self.version, self.data, self.output_path)

            assert result is True
            mock_save.assert_called_once()  # Ensure save is called once

    def test_export_no_data(self):
        """Tests exporting when data is empty, expecting False."""
        with patch("openpyxl.Workbook.save") as mock_save:
            result = self.strategy.export(self.date, self.version, [], self.output_path)

            assert result is False
            mock_save.assert_not_called()  # Should not save when no data

    def test_export_creates_correct_sheets(self):
        """Tests if the export creates the correct sheets and populates them."""
        with patch("openpyxl.Workbook.save") as mock_save, \
             patch("openpyxl.Workbook.create_sheet") as mock_create_sheet:

            mock_ws1 = MagicMock()
            mock_ws2 = MagicMock()
            mock_create_sheet.side_effect = lambda title: mock_ws1 if title == "portfolio_margin" else mock_ws2

            result = self.strategy.export(self.date, self.version, self.data, self.output_path)

            assert result is True
            mock_create_sheet.assert_any_call(title="portfolio_margin")
            mock_create_sheet.assert_any_call(title="drilldowns")
            mock_ws1.append.assert_called()  # Ensure headers are written
            mock_ws2.append.assert_called()  # Ensure headers are written

    def test_export_calls_populate_sheet(self):
        """Tests that _populate_sheet is called for both sheets."""
        with patch("openpyxl.Workbook.save") as mock_save, \
             patch.object(self.strategy, "_populate_sheet") as mock_populate_sheet:

            result = self.strategy.export(self.date, self.version, self.data, self.output_path)

            assert result is True
            assert mock_populate_sheet.call_count == 2  # One for each sheet

