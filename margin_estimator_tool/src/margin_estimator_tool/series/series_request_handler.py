"""
This module contains logic for retrieving data about series and giving
output to the user.
"""


from typing import Dict, Any, List
import os
from margin_estimator_tool.src.margin_estimator_tool.core.data_exporter import DataExporter
from margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base import RequestHandler
from margin_estimator_tool.src.margin_estimator_tool.core.filter_handler import FilterHandler


class SeriesRequestHandler(RequestHandler):
    """Handler for sending requests to the /series endpoint and exporting data."""

    EXTRAFIELDS = ["product_id", "contract_date", "contract_maturity", "expiry_maturity",
                   "call_put_flag", "exercise_price", "version_number", "iid",
                   "act_trade_unit_no", "days_to_expiration", "trade_unit_value",
                   "exercise_style_flag", "contract_frequency"]

    INT_VALUES = ["contract_date", "contract_maturity", "expiry_maturity",
                  "exercise_price", "iid", "act_trade_unit_no",
                  "days_to_expiration", "trade_unit_value"]

    def __init__(self,
                 date=None,
                 version=None,
                 timestamp=None,
                 to_excel=False,
                 export_dir=None,
                 to_json=False,
                 products=None,
                 type=None,
                 call_put_flag=None,
                 filters=None,
                 template=False,
                 max_tte=None,
                 min_tte=None
                 ):
        super().__init__()
        self.business_date = self._get_business_date(date, version)
        self.version = version == "LIVE"
        self.timestamp = timestamp if timestamp is not None else 0
        self.to_excel = to_excel
        self.to_json = to_json
        self.export_dir = export_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.products = products.split(',')
        self.type = type
        self.call_put_flag = call_put_flag
        self.filter_handler = FilterHandler(self.EXTRAFIELDS, self.INT_VALUES)
        self.filters = self.filter_handler.parse_filters(filters)
        self.template = template
        self.max_tte = max_tte
        self.min_tte = min_tte

    def process_and_provide_output(self) -> None:
        """Processes the data from /series and exports it according to the specified format."""
        series = self.send_request()
        filtered_series = self._filter_series(series)
        DataExporter.export(filtered_series,
                            "Series",
                            self.export_dir,
                            self.to_excel,
                            self.to_json,
                            str(self.business_date),
                            self.version)

        if self.template:
            self._generate_etd_portfolio_template(filtered_series)

    def send_request(self) -> List[Dict[str, Any]]:
        """Sends a GET request to the /series endpoint with optional filters, date, and version."""
        try:
            response = self.api.series_get(products=self.products,
                                           extrafields=self.EXTRAFIELDS,
                                           business_date=self.business_date,
                                           live_timestamp=self.timestamp,
                                           live=self.version)
            self._check_for_error_in_response(response)
            response = response.get("list_series", [])
            return response
        except Exception as e:
            self._handle_request_error(e)
        return []

    def _generate_etd_portfolio_template(self, filtered_series: List[Dict[str, Any]]) -> None:
        """Generates an ETD portfolio template based on the filtered series."""
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

        DataExporter.export(etd_portfolio,
                            "Template",
                            self.export_dir,
                            self.to_excel,
                            self.to_json,
                            str(self.business_date),
                            self.version)

    def _filter_series(self, series: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters the series based on various criteria."""

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
            "tte": tte_filter
        }

        filtered_series = self.filter_handler.filter_response(series, self.filters, custom_filters)

        return filtered_series
