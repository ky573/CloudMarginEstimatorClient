import os
from unittest.mock import patch, mock_open
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.csv_export_strategy import CSVExportStrategy


class TestCSVExportStrategy:
    """Test suite for the CSVExportStrategy class."""

    def setup_method(self):
        """Setup test data before each test."""
        self.strategy = CSVExportStrategy("products")
        self.date = "20250318"
        self.version = True
        self.output_path = "test_dir"
        self.data = [
            {"column1": "value1", "column2": "value2"},
            {"column1": "value3", "column2": "value4"},
        ]
        self.expected_filename = os.path.join(
            self.output_path, f"{self.date}_LIVE_products.csv"
        )

    def test_export_success(self):
        """Tests successful CSV export."""
        with patch("os.path.join", return_value="test_dir/test_file.csv") as mock_path_join, \
                patch("csv.DictWriter") as mock_dict_writer, \
                patch("builtins.open", new_callable=mock_open) as mock_file:
            mock_writer_instance = mock_dict_writer.return_value
            result = self.strategy.export(self.date, self.version, self.data, self.output_path)

            assert result is True
            mock_dict_writer.assert_called_once()
            mock_writer_instance.writeheader.assert_called_once()
            mock_writer_instance.writerows.assert_called_once_with(self.data)
            mock_file.assert_called_once_with("test_dir/test_file.csv", "w", newline="")

    def test_export_no_data(self):
        """Tests exporting with no data should return False."""
        with patch("builtins.open", mock_open()) as mock_file:
            result = self.strategy.export(self.date, self.version, [], self.output_path)

            assert result is False
            mock_file.assert_not_called()