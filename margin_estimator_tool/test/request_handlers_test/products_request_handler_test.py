"""Test suite for ProductsRequestHandler class."""

from unittest.mock import patch
import os
import pytest
from datetime import datetime
from products.products_request_handler import ProductsRequestHandler


class TestProductsRequestHandler:
    """Test cases for ProductsRequestHandler class."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        handler = ProductsRequestHandler()

        assert handler._version is False  # Default to EOD (not LIVE)
        assert handler._to_excel is False
        assert handler._to_json is False
        assert handler._timestamp == 0
        assert os.path.isabs(handler._export_dir)

    def test_init_with_custom_values(self):
        """Test initialization with custom values."""
        current_date = datetime.now().strftime("%Y%m%d")
        export_dir = "/tmp/exports"
        timestamp = 1234567890

        handler = ProductsRequestHandler(
            date=current_date,
            version="LIVE",
            to_excel=True,
            to_json=True,
            export_dir=export_dir,
            timestamp=timestamp,
            filters="currency:USD,product_type:OINX",
        )

        assert handler._business_date == int(current_date)
        assert handler._version is True  # LIVE
        assert handler._to_excel is True
        assert handler._to_json is True
        assert handler._export_dir == export_dir
        assert handler._timestamp == timestamp

    def test_init_parses_filters(self):
        """Test that filters are parsed during initialization."""
        with patch(
            "core.filter_handler.FilterHandler.parse_filters"
        ) as mock_parse_filters:
            mock_parse_filters.return_value = {
                "currency": "USD",
                "product_type": "OINX",
            }

            handler = ProductsRequestHandler(filters="currency:USD,product_type:OINX")

            mock_parse_filters.assert_called_once_with("currency:USD,product_type:OINX")
            assert handler._filters == {"currency": "USD", "product_type": "OINX"}

    def test_send_request_error(self):
        """Test that a trace_id in the response causes the program to exit."""
        fake_error_response = {"trace_id": "123456", "message": "some error"}

        with patch("core.request_handler_base.RequestHandler._setup_api") as mock_setup_api:
            mock_api = mock_setup_api.return_value
            mock_api.products_get.return_value = fake_error_response

            with patch("click.echo") as mock_echo:
                handler = ProductsRequestHandler(date="20250101")

                with pytest.raises(SystemExit) as e:
                    handler.send_request()

                assert e.value.code == 1
                mock_echo.assert_any_call("An error occurred in the request. Full response details:")

    def test_business_date_handling(self):
        """Test business date handling logic."""
        # Test with specific date
        handler = ProductsRequestHandler(date="20250101")
        assert handler._business_date == 20250101
