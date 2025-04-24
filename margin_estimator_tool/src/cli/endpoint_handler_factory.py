"""Factory module for creating endpoint handlers."""

from core.request_handler_base import RequestHandler
from products.products_request_handler import ProductsRequestHandler
from estimator.margin_calculator.margin_calculator_request_handler import MarginCalculatorRequestHandler
from series.series_request_handler import SeriesRequestHandler
from live_snapshots.live_snapshots_request_handler import LiveSnapshotRequestHandler
from snapshots.snapshots_request_handler import SnapshotRequestHandler
from estimator.etd_portfolio.etd_portfolio_request_handler import EtdPortfolioRequestHandler


class EndpointHandlerFactory:
    """Simple Factory for creating desired request handler based on CLI."""

    @staticmethod
    def get_handler(endpoint: str, **kwargs) -> RequestHandler:
        """
        Creates and returns desired handler.

        Args:
            endpoint: desired endpoint for which the concrete request handler will be created
            **kwargs: arguments from the CLI

        Returns:
            A concrete instance of the request handler

        Raises:
            ValueError: If no handler is defined for the given endpoint
        """
        handlers = {
            "margin_calculator": MarginCalculatorRequestHandler,
            "get_products": ProductsRequestHandler,
            "get_series": SeriesRequestHandler,
            "get_live_snapshots": LiveSnapshotRequestHandler,
            "get_snapshots": SnapshotRequestHandler,
            "etd_portfolio": EtdPortfolioRequestHandler,
        }

        handler_class = handlers.get(endpoint)
        if handler_class:
            return handler_class(**kwargs)
        else:
            raise ValueError(f"No handler defined for endpoint: {endpoint}")
