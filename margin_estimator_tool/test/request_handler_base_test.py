import pytest
from unittest.mock import patch, MagicMock, call
import requests
from datetime import datetime
from margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base import RequestHandler


# Create a concrete subclass for testing the abstract class
class ConcreteRequestHandler(RequestHandler):
    def process_and_provide_output(self) -> None:
        pass


class TestRequestHandler:
    """Test cases for RequestHandler base class."""

    def setup_method(self):
        """Set up a concrete handler instance for testing."""
        # Create with patch to avoid actual API setup
        with patch.object(RequestHandler, '_setup_api'):
            self.handler = ConcreteRequestHandler()

    @pytest.mark.parametrize(
        "error,expected_message", [
            (requests.exceptions.HTTPError("404 Not Found"), "HTTP Error: 404 Not Found"),
            (requests.exceptions.ConnectionError("Connection refused"), "Error sending request: Connection refused"),
            (ValueError("Invalid parameter"), "Error: Invalid parameter")
        ]
    )
    def test_handle_request_error(self, error, expected_message):
        """Test that _handle_request_error correctly handles different error types."""
        with patch('click.echo') as mock_echo:
            RequestHandler._handle_request_error(error)
            mock_echo.assert_called_once()
            assert expected_message in mock_echo.call_args[0][0]
            assert mock_echo.call_args[1].get('err', False) is True

    @pytest.mark.parametrize(
        "date,version,expected_date,is_weekend", [
            ("20250101", None, 20250101, False),  # Explicit date
            (None, "SOD", 20250311, False),  # SOD with weekday
            (None, "SOD", 20250310, True),  # SOD with weekend
            (None, "LIVE", 20250312, False),  # LIVE version
        ]
    )
    def test_get_business_date(self, date, version, expected_date, is_weekend):
        """Test that _get_business_date returns the correct date based on inputs."""
        mock_today = datetime(2025, 3, 12)  # Wednesday
        mock_yesterday = datetime(2025, 3, 11)  # Tuesday
        mock_weekend = datetime(2025, 3, 8)  # Saturday

        with patch('datetime.datetime') as mock_datetime, \
                patch.object(RequestHandler, '_is_business_day') as mock_is_business_day:

            mock_datetime.today.return_value = mock_today

            # Setup for SOD with weekend handling
            if version == "SOD" and is_weekend:
                mock_is_business_day.side_effect = [False, True]  # Weekend then weekday
            else:
                mock_is_business_day.return_value = True

            result = self.handler._get_business_date(date, version)
            assert result == expected_date

    def test_check_for_error_in_response_success(self):
        """Test that _check_for_error_in_response handles success correctly."""
        response = {"data": "some data"}

        with patch('click.echo') as mock_echo:
            RequestHandler._check_for_error_in_response(response)
            mock_echo.assert_called_once_with("Request successful.")

    def test_check_for_error_in_response_error(self):
        """Test that _check_for_error_in_response handles errors correctly."""
        response = {"trace_id": "abc123", "error": "Something went wrong"}

        with patch('click.echo') as mock_echo, \
                patch('sys.exit') as mock_exit:
            RequestHandler._check_for_error_in_response(response)

            assert mock_echo.call_count == 3
            mock_echo.assert_has_calls([
                call("An error occurred in the request. Full response details:"),
                call('{\n    "trace_id": "abc123",\n    "error": "Something went wrong"\n}')
            ])
            mock_exit.assert_called_once_with(1)

    @pytest.mark.parametrize(
        "weekday,expected", [
            (0, True),  # Monday
            (1, True),  # Tuesday
            (2, True),  # Wednesday
            (3, True),  # Thursday
            (4, True),  # Friday
            (5, False),  # Saturday
            (6, False),  # Sunday
        ]
    )
    def test_is_business_day(self, weekday, expected):
        """Test that _is_business_day correctly identifies business days."""
        date = MagicMock()
        date.weekday.return_value = weekday

        result = RequestHandler._is_business_day(date)
        assert result == expected