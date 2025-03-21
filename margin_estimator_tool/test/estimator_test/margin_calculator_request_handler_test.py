"""Test suite for MarginCalculatorRequestHandler class"""

from unittest.mock import patch, MagicMock
from margin_estimator_tool.src.margin_estimator_tool.estimator.margin_calculator.margin_calculator_request_handler import (
    MarginCalculatorRequestHandler,
)


class TestMarginCalculatorRequestHandler:
    """Test cases for the MarginCalculatorRequestHandler class."""

    def setup_method(self):
        """Setup initial test data."""
        self.csv_file = "portfolio.csv"
        self.version = "LIVE"
        self.timestamp = 1234567890
        self.date_from = "20250303"
        self.date_to = "20250305"
        self.export_dir = "test_output_dir"

        # Initialize handler instance
        self.handler = MarginCalculatorRequestHandler(
            csv_file=self.csv_file,
            version=self.version,
            timestamp=self.timestamp,
            date_from=self.date_from,
            date_to=self.date_to,
            export_dir=self.export_dir,
        )

    def test_initialization(self):
        """Test that the handler is initialized with correct attributes."""
        assert self.handler.csv_file == self.csv_file
        assert self.handler.version is True  # "LIVE" should map to True
        assert self.handler.timestamp == self.timestamp
        assert self.handler.date_from == self.date_from
        assert self.handler.date_to == self.date_to
        assert self.handler.export_dir == self.export_dir

    def test_process_and_provide_output_valid_headers(self):
        """Test that margin data is processed and exported when headers are valid."""
        mock_business_days = [20250303, 20250304]
        mock_margin_data = [{"margin": "data"}]

        with patch.object(self.handler.header_validator, "validate_headers", return_value=True), \
             patch.object(self.handler, "_collect_business_days", return_value=mock_business_days), \
             patch.object(self.handler, "_fetch_margin_data", return_value=mock_margin_data), \
             patch.object(self.handler, "_export_results") as mock_export_results:

            self.handler.process_and_provide_output()

            mock_export_results.assert_called_once_with(mock_margin_data)

    def test_process_and_provide_output_invalid_headers(self):
        """Test that processing stops if CSV header validation fails."""
        with patch.object(self.handler.header_validator, "validate_headers", return_value=False), \
             patch("click.echo") as mock_echo, \
             patch.object(self.handler, "_collect_business_days") as mock_collect_days:

            self.handler.process_and_provide_output()

            mock_echo.assert_called_once_with("Failed to validate CSV portfolio file. Process aborted.")
            mock_collect_days.assert_not_called()

    def test_send_request_successful_response(self):
        """Test sending a request with a successful response."""
        business_date = 20250303
        mock_response = {"portfolio": "data"}

        with patch.object(self.handler.request_builder, "build_request", return_value=MagicMock()), \
             patch.object(self.handler.api, "estimator_post", return_value=mock_response), \
             patch.object(self.handler, "_check_for_error_in_response") as mock_check:

            response = self.handler.send_request(business_date)

            assert response == mock_response
            mock_check.assert_called_once()

    def test_send_request_handles_exception(self):
        """Test handling an exception when the API request fails."""
        business_date = 20250303

        with patch.object(self.handler.request_builder, "build_request"), \
             patch.object(self.handler.api, "estimator_post", side_effect=Exception("API error")), \
             patch("click.echo") as mock_echo, \
             patch.object(self.handler, "_handle_request_error") as mock_handle_error:

            response = self.handler.send_request(business_date)

            assert response == {}  # Empty dictionary should be returned on error
            mock_echo.assert_called_once_with("Request failed for date 20250303.")
            mock_handle_error.assert_called_once()

    def test_collect_business_days(self):
        """Test collecting business days between date_from and date_to."""
        with patch.object(self.handler, "_is_business_day", side_effect=[True, False, True]):
            business_days = self.handler._collect_business_days()

            assert business_days == [20250303, 20250305]  # Should skip the second date (non-business)

    def test_export_results(self):
        """Test exporting the results using DataExporter and GraphExporter."""
        margin_data = [{"key": "value"}]

        with patch("margin_estimator_tool.src.margin_estimator_tool.core.data_exporter.DataExporter.export") as mock_data_export, \
             patch("margin_estimator_tool.src.margin_estimator_tool.estimator.margin_calculator.graph_exporter.GraphExporter.save_graph") as mock_save_graph:

            self.handler._export_results(margin_data)

            mock_data_export.assert_called_once_with(
                margin_data,
                "Margins",
                self.export_dir,
                True,
                False,
                self.date_from + "_" + self.date_to,
                True,  # version == "LIVE" -> True
            )
            mock_save_graph.assert_called_once()

    def test_fetch_margin_data(self):
        """Test fetching margin data for a list of business days."""
        business_days = [20250303, 20250304]
        mock_data = {"key": "value"}

        with patch.object(self.handler, "send_request", side_effect=[mock_data, {}]), \
             patch.object(self.handler.extractor, "extract_data") as mock_extract:

            margin_data = self.handler._fetch_margin_data(business_days)

            assert margin_data == [mock_data]  # Only the valid non-empty response should be included
            mock_extract.assert_called_once_with(mock_data)
