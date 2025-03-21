"""Test suite for EtdPortfolioCSVExportStrategy class."""

import os
from unittest.mock import patch, mock_open
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.etd_portfolio_csv_export_strategy import (
    EtdPortfolioCSVExportStrategy,
)


class TestEtdPortfolioCSVExportStrategy:
    """Test cases for the EtdPortfolioCSVExportStrategy class."""

    def setup_method(self):
        """Setup test data before each test."""
        self.strategy = EtdPortfolioCSVExportStrategy("estimator")
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
        self.expected_margin_filename = os.path.join(
            self.output_path, f"{self.date}_LIVE_portfolio_margin.csv"
        )
        self.expected_drilldowns_filename = os.path.join(
            self.output_path, f"{self.date}_LIVE_portfolio_drilldowns.csv"
        )

    def test_export_success(self):
        """Tests exporting portfolio data successfully to CSV."""
        with patch("builtins.open", mock_open()) as mock_file, patch(
            "csv.DictWriter"
        ) as mock_writer:
            mock_instance = mock_writer.return_value
            result = self.strategy.export(
                self.date, self.version, self.portfolio_data, self.output_path
            )

            assert result is True
            mock_file.assert_any_call(
                self.expected_margin_filename, "w", newline=""
            )
            mock_file.assert_any_call(
                self.expected_drilldowns_filename, "w", newline=""
            )
            assert mock_instance.writeheader.call_count == 2
            assert mock_instance.writerows.call_count == 2

    def test_export_no_data(self):
        """Tests exporting when portfolio data is empty, expecting False."""
        with patch("builtins.open", mock_open()) as mock_file, patch(
            "csv.DictWriter"
        ) as mock_writer:
            result = self.strategy.export(self.date, self.version, {}, self.output_path)

            assert result is False
            mock_file.assert_not_called()
            mock_writer.assert_not_called()

    def test_export_no_drilldowns(self):
        """Tests exporting when there are portfolio margins but no drilldowns."""
        data_no_drilldowns = {"portfolio_margin": self.portfolio_data["portfolio_margin"]}

        with patch("builtins.open", mock_open()) as mock_file, patch(
            "csv.DictWriter"
        ) as mock_writer:
            mock_instance = mock_writer.return_value
            result = self.strategy.export(
                self.date, self.version, data_no_drilldowns, self.output_path
            )

            assert result is True
            mock_file.assert_called_once_with(
                self.expected_margin_filename, "w", newline=""
            )
            mock_instance.writeheader.assert_called_once()
            mock_instance.writerows.assert_called_once()

    def test_export_no_portfolio_margin(self):
        """Tests exporting when there are drilldowns but no portfolio margins."""
        data_no_margins = {"drilldowns": self.portfolio_data["drilldowns"]}

        with patch("builtins.open", mock_open()) as mock_file, patch(
            "csv.DictWriter"
        ) as mock_writer:
            mock_instance = mock_writer.return_value
            result = self.strategy.export(
                self.date, self.version, data_no_margins, self.output_path
            )

            assert result is True
            mock_file.assert_called_once_with(
                self.expected_drilldowns_filename, "w", newline=""
            )
            mock_instance.writeheader.assert_called_once()
            mock_instance.writerows.assert_called_once()
