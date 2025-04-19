"""Test suite for ProductsRequestHandler class."""

from unittest.mock import patch
import os
from datetime import datetime
from margin_estimator_tool.src.margin_estimator_tool.products.products_request_handler import (
    ProductsRequestHandler,
)


class TestProductsRequestHandler:
    """Test cases for ProductsRequestHandler class."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        handler = ProductsRequestHandler()

        assert handler.version is False  # Default to EOD (not LIVE)
        assert handler.to_excel is False
        assert handler.to_json is False
        assert handler.timestamp == 0
        assert os.path.isabs(handler.export_dir)

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

        assert handler.business_date == int(current_date)
        assert handler.version is True  # LIVE
        assert handler.to_excel is True
        assert handler.to_json is True
        assert handler.export_dir == export_dir
        assert handler.timestamp == timestamp

    def test_init_parses_filters(self):
        """Test that filters are parsed during initialization."""
        with patch(
            "margin_estimator_tool.src.margin_estimator_tool.core.filter_handler.FilterHandler.parse_filters"
        ) as mock_parse_filters:
            mock_parse_filters.return_value = {
                "currency": "USD",
                "product_type": "OINX",
            }

            handler = ProductsRequestHandler(filters="currency:USD,product_type:OINX")

            mock_parse_filters.assert_called_once_with("currency:USD,product_type:OINX")
            assert handler.filters == {"currency": "USD", "product_type": "OINX"}

    def test_send_request_error(self):
        """Test API request with error response."""
        with patch(
            "margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base.RequestHandler.api",
            create=True,
        ) as mock_api:
            with patch("click.echo") as mock_echo, patch("sys.exit") as mock_exit:
                handler = ProductsRequestHandler(date="20250101")
                result = handler.send_request()

                # Verify that sys.exit(1) is called (program exits with exit code 1)
                mock_exit.assert_called_with(1)

                # Verify empty list returned on error
                assert result == []

    def test_business_date_handling(self):
        """Test business date handling logic."""
        # Test with specific date
        handler = ProductsRequestHandler(date="20250101")
        assert handler.business_date == 20250101
