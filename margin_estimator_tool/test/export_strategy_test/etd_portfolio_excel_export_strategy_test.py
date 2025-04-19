"""Test suite for the EtdPortfolioExcelExportStrategy class."""

import os
from unittest.mock import patch, MagicMock
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.etd_portfolio_excel_export_strategy import (
    EtdPortfolioExcelExportStrategy,
)


class TestEtdPortfolioExcelExportStrategy:
    """Test cases for the EtdPortfolioExcelExportStrategy class."""

    def setup_method(self):
        """Setup test data before each test."""
        self.strategy = EtdPortfolioExcelExportStrategy("estimator")
        self.date = "20250318"
        self.version = True
        self.output_path = "test_dir"
        self.portfolio_data = {
            "portfolio_margin": [
                {"key1": "value1", "key2": "value2"},
                {"key1": "value3", "key2": "value4"},
            ],
            "drilldowns": [
                {"drill_key1": "drill_value1", "drill_key2": "drill_value2"}
            ],
        }
        self.expected_filename = os.path.join(
            self.output_path, f"{self.date}_LIVE_portfolio.xlsx"
        )

    def test_export_success(self):
        """Tests exporting portfolio data successfully to an Excel file using openpyxl."""
        with patch("pandas.ExcelWriter", autospec=True) as mock_excel_writer, patch(
            "openpyxl.workbook.workbook.Workbook.save"
        ) as mock_save:
            mock_writer_instance = MagicMock()
            mock_excel_writer.return_value.__enter__.return_value = mock_writer_instance
            mock_save.return_value = None  # Prevents actual file saving

            result = self.strategy.export(
                self.date, self.version, self.portfolio_data, self.output_path
            )

            assert result is True
            mock_excel_writer.assert_called_once_with(
                self.expected_filename, engine="openpyxl"
            )
            mock_save.assert_called()

    def test_export_no_data(self):
        """Tests exporting when both portfolio_margin and drilldowns are empty, expecting False."""
        empty_data = {"portfolio_margin": [], "drilldowns": []}

        with patch("pandas.ExcelWriter", autospec=True) as mock_excel_writer, patch(
            "openpyxl.workbook.workbook.Workbook.save"
        ) as mock_save:
            mock_writer_instance = MagicMock()
            mock_excel_writer.return_value.__enter__.return_value = mock_writer_instance
            mock_save.return_value = None

            result = self.strategy.export(
                self.date, self.version, empty_data, self.output_path
            )

            assert result is False
            # mock_excel_writer.assert_called_once_with(
            #     self.expected_filename, engine="openpyxl"
            # )
            mock_excel_writer.assert_not_called()
            mock_save.assert_not_called()  # Should not save when no data

    def test_export_calls_submethods(self):
        """Tests that _export_margins and _export_drilldowns are called correctly."""
        with patch("pandas.ExcelWriter", autospec=True) as mock_excel_writer, patch(
            "openpyxl.workbook.workbook.Workbook.save"
        ) as mock_save, patch(
            "margin_estimator_tool.src.margin_estimator_tool.export_strategy.etd_portfolio_excel_export_strategy.EtdPortfolioExcelExportStrategy._export_margins"
        ) as mock_export_margins, patch(
            "margin_estimator_tool.src.margin_estimator_tool.export_strategy.etd_portfolio_excel_export_strategy.EtdPortfolioExcelExportStrategy._export_drilldowns"
        ) as mock_export_drilldowns:
            mock_export_margins.return_value = True
            mock_export_drilldowns.return_value = False
            mock_writer_instance = MagicMock()
            mock_excel_writer.return_value.__enter__.return_value = mock_writer_instance
            mock_save.return_value = None

            result = self.strategy.export(
                self.date, self.version, self.portfolio_data, self.output_path
            )

            assert result is True
            mock_export_margins.assert_called_once()
            mock_export_drilldowns.assert_called_once()
