"""Test suite for the DataExporter class."""

from unittest.mock import patch
from export_strategy.export_context import ExportContext
from core.data_exporter import DataExporter


class TestDataExporter:
    """Test suite for verifying the behavior of the DataExporter class."""

    def test_export_csv(self):
        """Test exporting data in CSV format."""
        with patch.object(ExportContext, "export_data", return_value=True):
            with patch("click.echo") as mock_echo:
                DataExporter.export(
                    [], "Products", "/tmp", False, False, "20250319", True
                )
                mock_echo.assert_called_with("Products exported to /tmp")

    def test_export_excel(self):
        """Test exporting data in Excel format."""
        with patch.object(ExportContext, "export_data", return_value=True):
            with patch("click.echo") as mock_echo:
                DataExporter.export(
                    [], "Products", "/tmp", True, False, "20250319", True
                )
                mock_echo.assert_called_with("Products exported to /tmp")

    def test_export_json(self):
        """Test exporting data in JSON format."""
        with patch.object(ExportContext, "export_data", return_value=True):
            with patch("click.echo") as mock_echo:
                DataExporter.export(
                    [], "Products", "/tmp", False, True, "20250319", True
                )
                mock_echo.assert_called_with("Products exported to /tmp")

    def test_export_no_data(self):
        """Test exporting when no data is available."""
        with patch.object(ExportContext, "export_data", return_value=False):
            with patch("click.echo") as mock_echo:
                DataExporter.export(
                    [], "Products", "/tmp", False, True, "20250319", True
                )
                mock_echo.assert_called_with("No data found.")

    def test_unknown_export_name(self):
        """Test exporting with an unknown export type name."""
        with patch.object(ExportContext, "export_data", return_value=True):
            with patch("click.echo") as mock_echo:
                DataExporter.export(
                    [], "Unknown export type", "/tmp", False, True, "20250319", True
                )
                mock_echo.assert_called_with(
                    "Export failed: Unknown export name: Unknown export type"
                )
