from unittest.mock import patch, MagicMock
from margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler import SnapshotRequestHandler


class TestSnapshotRequestHandler:
    """Tests for the SnapshotRequestHandler class."""

    @patch(
        'margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.RequestHandler._setup_api')
    def test_initialization(self, mock_setup_api):
        """Test that handler initializes correctly with proper values."""
        mock_setup_api.return_value = MagicMock()
        date_from = "20250301"
        date_to = "20250315"

        handler = SnapshotRequestHandler(date_from=date_from, date_to=date_to)

        assert handler.date_from == date_from
        assert handler.date_to == date_to
        mock_setup_api.assert_called_once()

    @patch(
        'margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.RequestHandler._setup_api')
    @patch('margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.datetime')
    def test_initialization_with_default_date_to(self, mock_datetime, mock_setup_api):
        """Test that handler uses current date when date_to is not provided."""
        mock_setup_api.return_value = MagicMock()
        mock_date = MagicMock()
        mock_date.strftime.return_value = "20250320"
        mock_datetime.now.return_value = mock_date
        date_from = "20250301"

        handler = SnapshotRequestHandler(date_from=date_from)

        assert handler.date_from == date_from
        assert handler.date_to == "20250320"
        mock_datetime.now.assert_called_once()

    @patch(
        'margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.RequestHandler._setup_api')
    @patch('margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.click')
    def test_process_and_provide_output_with_data(self, mock_click, mock_setup_api):
        """Test that handler processes and outputs data correctly."""
        mock_api = MagicMock()
        mock_setup_api.return_value = mock_api
        date_from = "20250301"
        date_to = "20250305"

        handler = SnapshotRequestHandler(date_from=date_from, date_to=date_to)

        # Create mock response with both live and non-live snapshots
        mock_snapshots = [
            {"business_date": "20250301", "live": False, "otc_available": True, "cash_available": False},
            {"business_date": "20250302", "live": False, "otc_available": False, "cash_available": True},
            {"business_date": "20250303", "live": True, "otc_available": True, "cash_available": True}
            # This should be filtered out
        ]

        # Mock send_request to return predefined snapshots
        handler.send_request = MagicMock(return_value=mock_snapshots)

        handler.process_and_provide_output()

        handler.send_request.assert_called_once()
        # Verify two calls to click.echo for the two non-live snapshots
        assert mock_click.echo.call_count == 2
        # Verify the content of the first call
        mock_click.echo.assert_any_call("  [01] date: 20250301 OTC=YES, CASH=NO")
        # Verify the content of the second call
        mock_click.echo.assert_any_call("  [02] date: 20250302 OTC=NO, CASH=YES")

    @patch(
        'margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.RequestHandler._setup_api')
    @patch(
        'margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.RequestHandler._check_for_error_in_response')
    def test_send_request_successful(self, mock_check_error, mock_setup_api):
        """Test that send_request correctly processes successful API response."""
        mock_api = MagicMock()
        mock_setup_api.return_value = mock_api

        expected_snapshots = [
            {"business_date": "20250301", "live": False, "otc_available": True, "cash_available": False}
        ]

        mock_api.snapshots_get.return_value = {"snapshots": expected_snapshots}

        handler = SnapshotRequestHandler(date_from="20250301", date_to="20250305")

        result = handler.send_request()

        mock_api.snapshots_get.assert_called_once_with(
            business_date_from="20250301",
            business_date_to="20250305"
        )
        mock_check_error.assert_called_once_with({"snapshots": expected_snapshots})
        assert result == expected_snapshots

    @patch(
        'margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.RequestHandler._setup_api')
    @patch(
        'margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.RequestHandler._handle_request_error')
    def test_send_request_exception(self, mock_handle_error, mock_setup_api):
        """Test that send_request correctly handles exceptions."""
        mock_api = MagicMock()
        mock_setup_api.return_value = mock_api

        # Set up the API to raise an exception
        test_exception = Exception("Test error")
        mock_api.snapshots_get.side_effect = test_exception

        handler = SnapshotRequestHandler(date_from="20250301", date_to="20250305")

        result = handler.send_request()

        mock_api.snapshots_get.assert_called_once_with(
            business_date_from="20250301",
            business_date_to="20250305"
        )
        mock_handle_error.assert_called_once_with(test_exception)
        assert result == []

    @patch('margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.click')
    def test_print_output(self, mock_click):
        """Test that _print_output formats and displays data correctly."""
        snapshots = [
            {"business_date": "20250301", "otc_available": True, "cash_available": False},
            {"business_date": "20250302", "otc_available": False, "cash_available": True},
            {"business_date": "20250303", "otc_available": True, "cash_available": True},
            {"business_date": "20250304"}  # Missing fields should default to "NO"
        ]

        SnapshotRequestHandler._print_output(snapshots)

        assert mock_click.echo.call_count == 4
        mock_click.echo.assert_any_call("  [01] date: 20250301 OTC=YES, CASH=NO")
        mock_click.echo.assert_any_call("  [02] date: 20250302 OTC=NO, CASH=YES")
        mock_click.echo.assert_any_call("  [03] date: 20250303 OTC=YES, CASH=YES")
        mock_click.echo.assert_any_call("  [04] date: 20250304 OTC=NO, CASH=NO")