from unittest.mock import patch
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.export_context import ExportContext
from margin_estimator_tool.src.margin_estimator_tool.core.data_exporter import DataExporter

class TestDataExporter:
    @patch.object(ExportContext, 'export_data', return_value=True)
    def test_export_csv(self, mock_export_data):
        with patch("click.echo") as mock_echo:
            DataExporter.export([], "Products", "/tmp", False, False, "20250319", True)
            mock_echo.assert_called_with("Products exported to /tmp")

    @patch.object(ExportContext, 'export_data', return_value=True)
    def test_export_excel(self, mock_export_data):
        with patch("click.echo") as mock_echo:
            DataExporter.export([], "Products", "/tmp", True, False, "20250319", True)
            mock_echo.assert_called_with("Products exported to /tmp")

    @patch.object(ExportContext, 'export_data', return_value=True)
    def test_export_json(self, mock_export_data):
        with patch("click.echo") as mock_echo:
            DataExporter.export([], "Products", "/tmp", False, True, "20250319", True)
            mock_echo.assert_called_with("Products exported to /tmp")

    @patch.object(ExportContext, 'export_data', return_value=False)
    def test_export_no_data(self, mock_export_data):
        with patch("click.echo") as mock_echo:
            DataExporter.export([], "Products", "/tmp", False, True, "20250319", True)
            mock_echo.assert_called_with("No data found.")

    @patch.object(ExportContext, 'export_data', return_value=True)
    def test_unknown_export_name(self, mock_export_data):
        with patch("click.echo") as mock_echo:
            DataExporter.export([], "Unknown export type", "/tmp", False, True, "20250319", True)
            mock_echo.assert_called_with("Export failed: Unknown export name: Unknown export type")