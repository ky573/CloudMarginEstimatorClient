"""
This module contains logic for retrieving information about products from
endpoint and then outputting them in desired format.
"""

from typing import Dict, Any, List, Optional
import os
from core.data_exporter import DataExporter
from core.request_handler_base import RequestHandler
from core.filter_handler import FilterHandler


class ProductsRequestHandler(RequestHandler):
    """Handler for sending requests to the /products endpoint and exporting data."""

    _EXTRAFIELDS = [
        "product",
        "instrument_type",
        "clearing_house",
        "prod_name",
        "prod_isin",
        "underlying_isin",
        "currency",
        "product_type",
        "extended_product_type",
        "margin_style_flag",
        "exercise_style_flag",
        "product_settlement_type",
        "final_settlement_time",
        "product_tick_size",
        "product_tick_value",
        "liquidation_group",
        "xm_eligibility",
    ]

    def __init__(
        self,
        date: Optional[str] = None,
        version: Optional[str] = None,
        to_excel: Optional[bool] = False,
        to_json: Optional[bool] = False,
        export_dir: Optional[str] = None,
        timestamp: Optional[int] = None,
        filters: Optional[str] = None,
    ) -> None:
        """
        Initializes the ProductsRequestHandler instance.

        Args:
            date: desired date, gets decided by function _get_business_date
            version: desired version in bool format, defaults to EOD
            to_excel: whether to export to excel
            to_json: whether to export to json
            export_dir: directory to export data to, defaults to root of the project
            timestamp: timestamp for request, defaults to 0
            filters: comma-separated string of key:values pairs for filtering
        """
        super().__init__()
        self._business_date = self._get_business_date(date, version)
        self._version = version == "LIVE"
        self._to_excel = to_excel
        self._to_json = to_json
        self._export_dir = export_dir or os.getcwd()
        self._timestamp = timestamp if timestamp is not None else 0
        self._filter_handler = FilterHandler(
            self._EXTRAFIELDS, ["product_tick_size", "product_tick_value"]
        )
        self._filters = self._filter_handler.parse_filters(filters)

    def process_and_provide_output(self) -> None:
        """Processes the data from /products and exports it according to the specified format."""
        products = self.send_request()
        filtered_products = self._filter_handler.filter_response(products, self._filters)
        DataExporter.export(
            filtered_products,
            "Products",
            self._export_dir,
            self._to_excel,
            self._to_json,
            str(self._business_date),
            self._version,
        )

    def send_request(self) -> List[Dict[str, Any]]:
        """
        Sends a GET request to /products endpoint with optional filters, date, and version.
        It also checks for the error in the response.

        Returns:
            response: Response returned from the endpoint containing data about products.
                      If an error is encountered during the request, it returns an empty list.
        """
        try:
            response = self._api.products_get(
                extrafields=self._EXTRAFIELDS,
                business_date=self._business_date,
                live_timestamp=self._timestamp,
                live=self._version,
            )
            self._check_for_error_in_response(response)
            response = response.get("products", [])
            return response
        except Exception as e:
            self._handle_request_error(e)
        return []
