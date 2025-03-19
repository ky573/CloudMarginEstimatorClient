"""
This module contains logic for retrieving data about series and giving
output to the user in desired format.
"""

from typing import Dict, Any, List, Optional
import os
from margin_estimator_tool.src.margin_estimator_tool.core.data_exporter import (
    DataExporter,
)
from margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base import (
    RequestHandler,
)
from margin_estimator_tool.src.margin_estimator_tool.core.filter_handler import (
    FilterHandler,
)


class SeriesRequestHandler(RequestHandler):
    """Handler for sending requests to the /series endpoint and exporting data."""

    EXTRAFIELDS = [
        "product_id",
        "contract_date",
        "contract_maturity",
        "expiry_maturity",
        "call_put_flag",
        "exercise_price",
        "version_number",
        "iid",
        "act_trade_unit_no",
        "days_to_expiration",
        "trade_unit_value",
        "exercise_style_flag",
        "contract_frequency",
    ]

    NUMERIC_VALUES = [
        "contract_date",
        "contract_maturity",
        "expiry_maturity",
        "exercise_price",
        "iid",
        "act_trade_unit_no",
        "days_to_expiration",
        "trade_unit_value",
    ]

    def __init__(
        self,
        date: Optional[str] = None,
        version: Optional[str] = None,
        timestamp: Optional[int] = None,
        to_excel: Optional[bool] = False,
        to_json: Optional[bool] = False,
        export_dir: Optional[str] = None,
        products: str = None,
        type: Optional[str] = None,
        call_put_flag: Optional[str] = None,
        filters: Optional[str] = None,
        template: Optional[bool] = False,
        max_tte: Optional[int] = None,
        min_tte: Optional[int] = None,
    ) -> None:
        """
        Initializes the SeriesRequestHandler instance.

        Args:
            business_date: desired business date for request, determined by function _get_business_date
            version: required version, gets converted to bool, defaults to SOD
            timestamp: timestamp for the data, defaults to 0
            to_excel: determines whether to export to excel
            to_json: determined whether to export to json
            export_dir: place to export data, if not specified, defaults to root of the project
            products: list of comma-separated list of products for request
            type: option or future, for filtering
            call_put_flag: C or P, for filtering
            filter_handler: class for handling of the filtering of the data
            filters: comma-separated list of filters, parsed by filter_handler
            template: decides whether to generate template for portfolio
            max_tte: maximum day_to_expiratoin, for filtering
            min_tte: minimum day_to_expiration, for filtering
        """
        super().__init__()
        self.business_date = self._get_business_date(date, version)
        self.version = version == "LIVE"
        self.timestamp = timestamp if timestamp is not None else 0
        self.to_excel = to_excel
        self.to_json = to_json
        self.export_dir = export_dir or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
        self.products = products.split(",")
        self.type = type
        self.call_put_flag = call_put_flag
        self.filter_handler = FilterHandler(self.EXTRAFIELDS, self.NUMERIC_VALUES)
        self.filters = self.filter_handler.parse_filters(filters)
        self.template = template
        self.max_tte = max_tte
        self.min_tte = min_tte

    def process_and_provide_output(self) -> None:
        """
        Processes the data from /series and exports it according to the specified format.

        If a template for portfolio is also requested, it generates it.
        """
        series = self.send_request()
        filtered_series = self._filter_series(series)
        DataExporter.export(
            filtered_series,
            "Series",
            self.export_dir,
            self.to_excel,
            self.to_json,
            str(self.business_date),
            self.version,
        )

        if self.template:
            self._generate_etd_portfolio_template(filtered_series)

    def send_request(self) -> List[Dict[str, Any]]:
        """
        Sends a GET request to the /series endpoint with optional filters, date, and version.
        It also checks for the error in the response.

        Returns:
            response: list of data from series endpoint.
                      Returns empty list in case of error in the response.
        """
        try:
            response = self.api.series_get(
                products=self.products,
                extrafields=self.EXTRAFIELDS,
                business_date=self.business_date,
                live_timestamp=self.timestamp,
                live=self.version,
            )
            self._check_for_error_in_response(response)
            response = response.get("list_series", [])
            return response
        except Exception as e:
            self._handle_request_error(e)
        return []

    def _generate_etd_portfolio_template(
        self, filtered_series: List[Dict[str, Any]]
    ) -> None:
        """
        Generates an ETD portfolio template based on the filtered series.

        Works by pulling out desired fields from the response so that the header is matched.
        Net LS Balance will need to be filled in manually, otherwise defaults to 0.
        """
        etd_portfolio = [
            {
                "Product ID": s["product_id"],
                "Contract Date": s["contract_date"],
                "Call Put Flag": s["call_put_flag"],
                "Exercise Price": s["exercise_price"],
                "Version Number": s["version_number"],
                "Net LS Balance": "",  # Empty for manual input
            }
            for s in filtered_series
        ]

        DataExporter.export(
            etd_portfolio,
            "Template",
            self.export_dir,
            self.to_excel,
            self.to_json,
            str(self.business_date),
            self.version,
        )

    def _filter_series(self, series: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filters the series based on various criteria, currently filters by
        call_put_flag, type and tte.

        Can be customized by adding more filters as callables.
        """

        def call_put_filter(series_: Dict[str, Any]) -> bool:
            """Filter for call_put_flag."""
            if not self.call_put_flag:
                return True
            return series_.get("call_put_flag") == self.call_put_flag

        def type_filter(series_: Dict[str, Any]) -> bool:
            """Filter for 'type' - options or futures."""
            if self.type == "option":
                return series_.get("call_put_flag") is not None
            if self.type == "future":
                return series_.get("call_put_flag") is None
            return True

        def tte_filter(series_: Dict[str, Any]) -> bool:
            """Filter for 'days_to_expiration'."""
            days_to_expiration = series_.get("days_to_expiration")
            if days_to_expiration is None:
                return False

            if self.max_tte is not None and days_to_expiration > self.max_tte:
                return False
            if self.min_tte is not None and days_to_expiration < self.min_tte:
                return False

            return True

        custom_filters = {
            "call_put_flag": call_put_filter,
            "type": type_filter,
            "tte": tte_filter,
        }

        filtered_series = self.filter_handler.filter_response(
            series, self.filters, custom_filters
        )

        return filtered_series
