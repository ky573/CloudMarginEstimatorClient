"""Test suite for the JSONExportStrategy class."""

import os
from unittest.mock import mock_open, patch
from export_strategy.json_export_strategy import JSONExportStrategy


class TestJSONExportStrategy:
    """Test cases for the JSONExportStrategy class."""

    def setup_method(self):
        """Setup test data before each test."""
        self.strategy = JSONExportStrategy("products")
        self.date = "20250318"
        self.version = True
        self.output_path = "test_dir"
        self.data = [
            {"key1": "value1", "key2": "value2"},
            {"key1": "value3", "key2": "value4"},
        ]
        self.expected_filename = os.path.join(
            self.output_path, f"{self.date}_LIVE_products.json"
        )

    def test_export_success(self):
        """Tests exporting data successfully to a JSON file."""
        with patch("builtins.open", mock_open()) as mock_file, patch(
            "json.dump"
        ) as mock_json_dump:
            result = self.strategy.export(
                self.date, self.version, self.data, self.output_path
            )

            assert result is True
            mock_file.assert_called_once_with(self.expected_filename, "w")
            mock_json_dump.assert_called_once_with(self.data, mock_file(), indent=4)

    def test_export_no_data(self):
        """Tests exporting when data is empty, expecting False."""
        with patch("builtins.open", mock_open()) as mock_file:
            result = self.strategy.export(self.date, self.version, [], self.output_path)

            assert result is False
            mock_file.assert_not_called()
