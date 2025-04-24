"""Test suite for EtdPortfolioRequestHandler class"""

from unittest.mock import patch, MagicMock
from estimator.etd_portfolio.etd_portfolio_request_handler import (
    EtdPortfolioRequestHandler,
)


class TestEtdPortfolioRequestHandler:
    """Test cases for the EtdPortfolioRequestHandler class."""

    def setup_method(self):
        """Setup test data before each test."""
        self.csv_file = "portfolio.csv"
        self.date = "20250318"
        self.version = "LIVE"
        self.timestamp = 1234567890
        self.to_excel = True
        self.to_json = False
        self.export_dir = "test_output_dir"

        # Create a handler instance for testing
        self.handler = EtdPortfolioRequestHandler(
            csv_file=self.csv_file,
            date=self.date,
            version=self.version,
            timestamp=self.timestamp,
            to_excel=self.to_excel,
            to_json=self.to_json,
            export_dir=self.export_dir,
        )

    def test_initialization(self):
        """Test that the handler is initialized with the correct parameters."""
        assert self.handler._csv_file == self.csv_file
        assert self.handler._business_date == int(self.date)
        assert self.handler._version is True  # "LIVE" should map to True
        assert self.handler._timestamp == self.timestamp
        assert self.handler._to_excel == self.to_excel
        assert self.handler._to_json == self.to_json
        assert self.handler._export_dir == self.export_dir

    def test_process_and_provide_output_valid_headers(self):
        """Test that data is processed and exported when headers are valid."""
        with patch.object(
            self.handler._header_validator, "validate_headers", return_value=True
        ), patch.object(
            self.handler, "send_request", return_value={"portfolio": "data"}
        ), patch(
            "core.data_exporter.DataExporter.export"
        ) as mock_export:

            self.handler.process_and_provide_output()

            mock_export.assert_called_once_with(
                {"portfolio": "data"},
                "Portfolio",
                self.export_dir,
                self.to_excel,
                self.to_json,
                str(self.date),
                True,
            )

    def test_process_and_provide_output_invalid_headers(self):
        """Test that no data is processed when headers are invalid."""
        with patch.object(
            self.handler._header_validator, "validate_headers", return_value=False
        ), patch("click.echo") as mock_echo, patch.object(
            self.handler, "send_request"
        ) as mock_send_request:

            self.handler.process_and_provide_output()

            mock_echo.assert_called_once_with(
                "Failed to validate CSV portfolio file. Process aborted."
            )
            mock_send_request.assert_not_called()  # send_request should not be called when headers are invalid

    def test_send_request_successful_response(self):
        """Test sending a request when the response contains valid data."""
        mock_response = MagicMock()
        mock_response.to_dict.return_value = {"key": "value"}

        with patch.object(
            self.handler._request_builder, "build_request", return_value=mock_response
        ), patch.object(
            self.handler._api, "estimator_post", return_value={"portfolio": "data"}
        ), patch.object(
            self.handler, "_check_for_error_in_response"
        ) as mock_check_error:

            response = self.handler.send_request()

            assert response == {"portfolio": "data"}
            mock_check_error.assert_called_once()  # Ensure response is validated

    def test_send_request_handles_exception(self):
        """Test handling an exception when the API request fails."""
        with patch.object(self.handler._request_builder, "build_request"), patch.object(
            self.handler._api, "estimator_post", side_effect=Exception("API error")
        ), patch.object(self.handler, "_handle_request_error") as mock_handle_error:

            response = self.handler.send_request()

            assert response == {}  # Empty dictionary should be returned on error
            mock_handle_error.assert_called_once()  # Ensure error handling is called
