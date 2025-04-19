"""Factory module for creating endpoint handlers."""

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
