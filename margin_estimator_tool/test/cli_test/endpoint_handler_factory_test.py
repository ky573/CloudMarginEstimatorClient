"""Test suite for EndpointHandlerFactory class."""

import pytest
from margin_estimator_tool.cli.endpoint_handler_factory import (
    EndpointHandlerFactory,
)
from margin_estimator_tool.core.request_handler_base import (
    RequestHandler,
)
from margin_estimator_tool.products.products_request_handler import (
    ProductsRequestHandler,
)
from margin_estimator_tool.estimator.margin_calculator.margin_calculator_request_handler import (
    MarginCalculatorRequestHandler,
)
from margin_estimator_tool.series.series_request_handler import (
    SeriesRequestHandler,
)
from margin_estimator_tool.live_snapshots.live_snapshots_request_handler import (
    LiveSnapshotRequestHandler,
)
from margin_estimator_tool.snapshots.snapshots_request_handler import (
    SnapshotRequestHandler,
)
from margin_estimator_tool.estimator.etd_portfolio.etd_portfolio_request_handler import (
    EtdPortfolioRequestHandler,
)


class TestEndpointHandlerFactory:
    """Test cases for EndpointHandlerFactory class."""

    def test_get_handler_margin_calculator(self):
        """Test that margin_calculator endpoint returns correct handler instance with all kwargs."""
        kwargs = {
            "csv_file": "/path/to/file.csv",
            "version": "EOD",
            "timestamp": "123456789",
            "date_from": "20250101",
            "date_to": "20250131",
            "export_dir": "/path/to/export",
        }

        handler = EndpointHandlerFactory.get_handler("margin_calculator", **kwargs)
        assert isinstance(handler, MarginCalculatorRequestHandler)
        assert isinstance(handler, RequestHandler)

    def test_get_handler_get_products(self):
        """Test that get_products endpoint returns correct handler instance with all kwargs."""
        kwargs = {
            "date": "20250101",
            "version": "LIVE",
            "to_excel": True,
            "to_json": False,
            "export_dir": "/path/to/export",
            "timestamp": 123456789,
            "filters": "clearing_house:EUXCDEFF,currency:CHF",
        }

        handler = EndpointHandlerFactory.get_handler("get_products", **kwargs)
        assert isinstance(handler, ProductsRequestHandler)
        assert isinstance(handler, RequestHandler)

    def test_get_handler_get_series(self):
        """Test that get_series endpoint returns correct handler instance with all kwargs."""
        kwargs = {
            "date": "20250101",
            "version": "EOD",
            "timestamp": 123456789,
            "to_excel": True,
            "to_json": False,
            "export_dir": "/path/to/export",
            "products": "BMW,AAPL",
            "type": "option",
            "call_put_flag": "C",
            "filters": "contract_date:20250321,days_to_expiration:50",
            "template": True,
            "max_tte": 90,
            "min_tte": 30,
        }

        handler = EndpointHandlerFactory.get_handler("get_series", **kwargs)
        assert isinstance(handler, SeriesRequestHandler)
        assert isinstance(handler, RequestHandler)

    def test_get_handler_get_live_snapshots(self):
        """Test that get_live_snapshots endpoint returns correct handler instance with all kwargs."""
        kwargs = {"date": "20250101"}

        handler = EndpointHandlerFactory.get_handler("get_live_snapshots", **kwargs)
        assert isinstance(handler, LiveSnapshotRequestHandler)
        assert isinstance(handler, RequestHandler)

    def test_get_handler_get_snapshots(self):
        """Test that get_snapshots endpoint returns correct handler instance with all kwargs."""
        kwargs = {"date_from": "20250101", "date_to": "20250131"}

        handler = EndpointHandlerFactory.get_handler("get_snapshots", **kwargs)
        assert isinstance(handler, SnapshotRequestHandler)
        assert isinstance(handler, RequestHandler)

    def test_get_handler_etd_portfolio(self):
        """Test that etd_portfolio endpoint returns correct handler instance with all kwargs."""
        kwargs = {
            "csv_file": "/path/to/portfolio.csv",
            "date": "20250101",
            "version": "EOD",
            "timestamp": 123456789,
            "to_excel": True,
            "to_json": False,
            "export_dir": "/path/to/export",
        }

        handler = EndpointHandlerFactory.get_handler("etd_portfolio", **kwargs)
        assert isinstance(handler, EtdPortfolioRequestHandler)
        assert isinstance(handler, RequestHandler)

    def test_get_handler_invalid_endpoint(self):
        """Test that invalid endpoint raises ValueError."""
        with pytest.raises(ValueError) as excinfo:
            EndpointHandlerFactory.get_handler("invalid_endpoint")

        assert "No handler defined for endpoint: invalid_endpoint" in str(excinfo.value)
