import pytest
from unittest.mock import patch, MagicMock
from margin_estimator_tool.src.margin_estimator_tool.live_snapshots.live_snapshots_request_handler import \
    LiveSnapshotRequestHandler


class TestLiveSnapshotRequestHandler:
    """Tests for the LiveSnapshotRequestHandler class."""

    @patch(
        'margin_estimator_tool.src.margin_estimator_tool.live_snapshots.live_snapshots_request_handler.RequestHandler._setup_api')
    def test_initialization(self, mock_setup_api):
        """Test that handler initializes correctly with proper values."""
        mock_setup_api.return_value = MagicMock()
        date = "20250301"

        handler = LiveSnapshotRequestHandler(date=date)

        assert handler.business_date == 20250301  # Check that string date is converted to int
        mock_setup_api.assert_called_once()

    @patch(
        'margin_estimator_tool.src.margin_estimator_tool.live_snapshots.live_snapshots_request_handler.RequestHandler._setup_api')
    @patch('margin_estimator_tool.src.margin_estimator_tool.live_snapshots.live_snapshots_request_handler.click')
    def test_process_and_provide_output(self, mock_click, mock_setup_api):
        """Test that handler processes and outputs data correctly."""
        mock_api = MagicMock()
        mock_setup_api.return_value = mock_api
        date = "20250301"

        handler = LiveSnapshotRequestHandler(date=date)

        # Create mock response with live snapshots
        mock_snapshots = [
            {"live_timestamp": "1709308800000", "otc_available": True, "cash_available": False},
            {"live_timestamp": "1709395200000", "otc_available": False, "cash_available": True},
            {"live_timestamp": 0, "otc_available": True, "cash_available": True}
        ]

        # Mock send_request to return predefined snapshots
        handler.send_request = MagicMock(return_value=mock_snapshots)

        handler.process_and_provide_output()

        handler.send_request.assert_called_once()
        mock_click.echo.assert_any_call("Available live snapshots for 20250301:")
        assert mock_click.echo.call_count == 4

    @patch(
        'margin_estimator_tool.src.margin_estimator_tool.live_snapshots.live_snapshots_request_handler.RequestHandler._setup_api')
    @patch(
        'margin_estimator_tool.src.margin_estimator_tool.live_snapshots.live_snapshots_request_handler.RequestHandler._check_for_error_in_response')
    def test_send_request_successful(self, mock_check_error, mock_setup_api):
        """Test that send_request correctly processes successful API response."""
        mock_api = MagicMock()
        mock_setup_api.return_value = mock_api

        expected_snapshots = [
            {"live_timestamp": "1709308800000", "otc_available": True, "cash_available": False}
        ]

        mock_api.live_snapshots_get.return_value = {"snapshots": expected_snapshots}

        handler = LiveSnapshotRequestHandler(date="20250301")

        result = handler.send_request()

        mock_api.live_snapshots_get.assert_called_once_with(business_date=20250301)
        mock_check_error.assert_called_once_with({"snapshots": expected_snapshots})
        assert result == expected_snapshots

    @patch(
        'margin_estimator_tool.src.margin_estimator_tool.live_snapshots.live_snapshots_request_handler.RequestHandler._setup_api')
    @patch(
        'margin_estimator_tool.src.margin_estimator_tool.live_snapshots.live_snapshots_request_handler.RequestHandler._handle_request_error')
    def test_send_request_exception(self, mock_handle_error, mock_setup_api):
        """Test that send_request correctly handles exceptions."""
        mock_api = MagicMock()
        mock_setup_api.return_value = mock_api

        # Set up the API to raise an exception
        test_exception = Exception("Test error")
        mock_api.live_snapshots_get.side_effect = test_exception

        handler = LiveSnapshotRequestHandler(date="20250301")

        result = handler.send_request()

        mock_api.live_snapshots_get.assert_called_once_with(business_date=20250301)
        mock_handle_error.assert_called_once_with(test_exception)
        assert result == []

    @patch('margin_estimator_tool.src.margin_estimator_tool.live_snapshots.live_snapshots_request_handler.click')
    @patch('margin_estimator_tool.src.margin_estimator_tool.live_snapshots.live_snapshots_request_handler.datetime')
    def test_print_output(self, mock_datetime, mock_click):
        """Test that _print_output formats and displays data correctly."""
        date = "20250301"
        handler = LiveSnapshotRequestHandler(date=date)

        # Mock the datetime.fromtimestamp function to return predictable times
        mock_formatted_time1 = MagicMock()
        mock_formatted_time1.strftime.return_value = "12:00:00"

        mock_formatted_time2 = MagicMock()
        mock_formatted_time2.strftime.return_value = "15:30:00"

        # Set up side effects to return different formatted times
        mock_datetime.fromtimestamp.side_effect = [mock_formatted_time1, mock_formatted_time2]

        snapshots = [
            {"live_timestamp": "1709308800000", "otc_available": True, "cash_available": False},
            {"live_timestamp": "1709395200000", "otc_available": False, "cash_available": True},
            {"live_timestamp": 0, "otc_available": True, "cash_available": True},
        ]

        handler._print_output(snapshots)

        # Check the header
        mock_click.echo.assert_any_call("Available live snapshots for 20250301:")

        # Check individual snapshot outputs for valid values
        mock_click.echo.assert_any_call("  [01] time: 12:00:00 ts:1709308800000 OTC=YES, CASH=NO")
        mock_click.echo.assert_any_call("  [02] time: 15:30:00 ts:1709395200000 OTC=NO, CASH=YES")
        mock_click.echo.assert_any_call("  [03] time: 0 ts:0 OTC=YES, CASH=YES")

        # Verify datetime.fromtimestamp was called correctly for valid timestamps
        mock_datetime.fromtimestamp.assert_any_call(1709308800)  # 1709308800000 / 1000
        mock_datetime.fromtimestamp.assert_any_call(1709395200)  # 1709395200000 / 1000

        # Verify that we called echo for each snapshot plus the header
        assert mock_click.echo.call_count == 4

    @patch(
        'margin_estimator_tool.src.margin_estimator_tool.live_snapshots.live_snapshots_request_handler.RequestHandler._setup_api')
    @patch('margin_estimator_tool.src.margin_estimator_tool.live_snapshots.live_snapshots_request_handler.click')
    def test_process_and_provide_output_with_empty_result(self, mock_click, mock_setup_api):
        """Test that handler handles empty result lists correctly."""
        mock_setup_api.return_value = MagicMock()
        date = "20250301"

        handler = LiveSnapshotRequestHandler(date=date)

        # Mock send_request to return empty list
        handler.send_request = MagicMock(return_value=[])

        handler.process_and_provide_output()

        handler.send_request.assert_called_once()
        # Verify only the header message is displayed
        mock_click.echo.assert_called_once_with("Available live snapshots for 20250301:")