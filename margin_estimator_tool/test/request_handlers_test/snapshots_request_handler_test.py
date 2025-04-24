"""Test suite for the SnapshotRequestHandler class."""

from unittest.mock import patch, MagicMock
from margin_estimator_tool.snapshots.snapshots_request_handler import (
    SnapshotRequestHandler,
)


class TestSnapshotRequestHandler:
    """Test cases for the SnapshotRequestHandler class."""

    def test_initialization(self):
        """Test that handler initializes correctly with proper values."""
        with patch(
            "margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.RequestHandler._setup_api"
        ) as mock_setup_api:
            mock_setup_api.return_value = MagicMock()
            date_from = "20250301"
            date_to = "20250315"

            handler = SnapshotRequestHandler(date_from=date_from, date_to=date_to)

            assert handler._date_from == date_from
            assert handler._date_to == date_to
            mock_setup_api.assert_called_once()

    def test_initialization_with_default_date_to(self):
        """Test that handler uses current date when date_to is not provided."""
        with patch(
            "margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.RequestHandler._setup_api"
        ) as mock_setup_api:
            with patch(
                "margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.datetime"
            ) as mock_datetime:
                mock_setup_api.return_value = MagicMock()
                mock_date = MagicMock()
                mock_date.strftime.return_value = "20250320"
                mock_datetime.now.return_value = mock_date
                date_from = "20250301"

                handler = SnapshotRequestHandler(date_from=date_from)

                assert handler._date_from == date_from
                assert handler._date_to == "20250320"
                mock_datetime.now.assert_called_once()

    def test_process_and_provide_output_with_data(self):
        """Test that handler processes and outputs data correctly."""
        with patch(
            "margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.RequestHandler._setup_api"
        ) as mock_setup_api:
            with patch(
                "margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.click"
            ) as mock_click:
                mock_api = MagicMock()
                mock_setup_api.return_value = mock_api
                date_from = "20250301"
                date_to = "20250305"

                handler = SnapshotRequestHandler(date_from=date_from, date_to=date_to)

                # Create mock response with both live and non-live snapshots
                mock_snapshots = [
                    {
                        "business_date": "20250301",
                        "live": False,
                        "otc_available": True,
                        "cash_available": False,
                    },
                    {
                        "business_date": "20250302",
                        "live": False,
                        "otc_available": False,
                        "cash_available": True,
                    },
                    {
                        "business_date": "20250303",
                        "live": True,
                        "otc_available": True,
                        "cash_available": True,
                    },
                    # This should be filtered out
                ]

                # Mock send_request to return predefined snapshots
                handler.send_request = MagicMock(return_value=mock_snapshots)

                handler.process_and_provide_output()

                handler.send_request.assert_called_once()
                # Verify two calls to click.echo for the two non-live snapshots
                assert mock_click.echo.call_count == 2
                # Verify the content of the first call
                mock_click.echo.assert_any_call(
                    "  [01] date: 20250301 OTC=YES, CASH=NO"
                )
                # Verify the content of the second call
                mock_click.echo.assert_any_call(
                    "  [02] date: 20250302 OTC=NO, CASH=YES"
                )

    def test_send_request_successful(self):
        """Test that send_request correctly processes successful API response."""
        with patch(
            "margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.RequestHandler._setup_api"
        ) as mock_setup_api:
            with patch(
                "margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.RequestHandler._check_for_error_in_response"
            ) as mock_check_error:
                mock_api = MagicMock()
                mock_setup_api.return_value = mock_api

                expected_snapshots = [
                    {
                        "business_date": "20250301",
                        "live": False,
                        "otc_available": True,
                        "cash_available": False,
                    }
                ]

                mock_api.snapshots_get.return_value = {"snapshots": expected_snapshots}

                handler = SnapshotRequestHandler(
                    date_from="20250301", date_to="20250305"
                )

                result = handler.send_request()

                mock_api.snapshots_get.assert_called_once_with(
                    business_date_from="20250301", business_date_to="20250305"
                )
                mock_check_error.assert_called_once_with(
                    {"snapshots": expected_snapshots}
                )
                assert result == expected_snapshots

    def test_send_request_exception(self):
        """Test that send_request correctly handles exceptions."""
        with patch(
            "margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.RequestHandler._setup_api"
        ) as mock_setup_api:
            with patch(
                "margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.RequestHandler._handle_request_error"
            ) as mock_handle_error:
                mock_api = MagicMock()
                mock_setup_api.return_value = mock_api

                # Set up the API to raise an exception
                test_exception = Exception("Test error")
                mock_api.snapshots_get.side_effect = test_exception

                handler = SnapshotRequestHandler(
                    date_from="20250301", date_to="20250305"
                )

                result = handler.send_request()

                mock_api.snapshots_get.assert_called_once_with(
                    business_date_from="20250301", business_date_to="20250305"
                )
                mock_handle_error.assert_called_once_with(test_exception)
                assert result == []

    def test_print_output(self):
        """Test that _print_output formats and displays data correctly."""
        with patch(
            "margin_estimator_tool.src.margin_estimator_tool.snapshots.snapshots_request_handler.click"
        ) as mock_click:
            snapshots = [
                {
                    "business_date": "20250301",
                    "otc_available": True,
                    "cash_available": False,
                },
                {
                    "business_date": "20250302",
                    "otc_available": False,
                    "cash_available": True,
                },
                {
                    "business_date": "20250303",
                    "otc_available": True,
                    "cash_available": True,
                },
                {"business_date": "20250304"},  # Missing fields should default to "NO"
            ]

            SnapshotRequestHandler._print_output(snapshots)

            assert mock_click.echo.call_count == 4
            mock_click.echo.assert_any_call("  [01] date: 20250301 OTC=YES, CASH=NO")
            mock_click.echo.assert_any_call("  [02] date: 20250302 OTC=NO, CASH=YES")
            mock_click.echo.assert_any_call("  [03] date: 20250303 OTC=YES, CASH=YES")
            mock_click.echo.assert_any_call("  [04] date: 20250304 OTC=NO, CASH=NO")
