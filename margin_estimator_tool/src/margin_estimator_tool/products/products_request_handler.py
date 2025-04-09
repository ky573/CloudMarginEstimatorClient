"""
This module contains logic for retrieving information about products from
endpoint and then outputting them in desired format.
"""

import json
from typing import Dict, Any, List, Optional
import os
from margin_estimator_tool.core.data_exporter import (
    DataExporter,
)
from margin_estimator_tool.core.request_handler_base import (
    RequestHandler,
)
from margin_estimator_tool.core.filter_handler import (
    FilterHandler,
)


class ProductsRequestHandler(RequestHandler):
    """Handler for sending requests to the /products endpoint and exporting data."""

    EXTRAFIELDS = [
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
            business_date: desired date, gets decied by function _get_business_date
            version: desired version in bool format, defaults to SOD
            to_excel: whether to export to excel
            to_json: whether to export to json
            export_dir: directory to export data to, defaults to root of the project
            timestamp: timestamp for request, defaults to 0
            filter_handler: instance of FilterHandler class, takes care of filters
            filters: comma-separeted string of key:values pairs for filtering
        """
        super().__init__()
        self.business_date = self._get_business_date(date, version)
        self.version = version == "LIVE"
        self.to_excel = to_excel
        self.to_json = to_json
        self.export_dir = export_dir or os.getcwd()
        self.timestamp = timestamp if timestamp is not None else 0
        self.filter_handler = FilterHandler(
            self.EXTRAFIELDS, ["product_tick_size", "product_tick_value"]
        )
        self.filters = self.filter_handler.parse_filters(filters)

    def process_and_provide_output(self) -> None:
        """Processes the data from /products and exports it according to the specified format."""
        products = self.send_request()
        filtered_products = self.filter_handler.filter_response(products, self.filters)
        DataExporter.export(
            filtered_products,
            "Products",
            self.export_dir,
            self.to_excel,
            self.to_json,
            str(self.business_date),
            self.version,
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
            response = self.api.products_get(
                extrafields=self.EXTRAFIELDS,
                business_date=self.business_date,
                live_timestamp=self.timestamp,
                live=self.version,
            )
            self._check_for_error_in_response(response)
            response = response.get("products", [])
            return response
        except Exception as e:
            self._handle_request_error(e)
        return []
