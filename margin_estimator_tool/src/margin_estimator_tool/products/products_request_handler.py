"""
This module contains logic for retrieving information about products from
endpoint and then outputting them in desired form.
"""

from typing import Dict, Any, List
import os
from margin_estimator_tool.src.margin_estimator_tool.core.data_exporter import DataExporter
from margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base import RequestHandler
from margin_estimator_tool.src.margin_estimator_tool.core.filter_handler import FilterHandler


EXTRAFIELDS = ['product', 'instrument_type', 'clearing_house', 'prod_name', 'prod_isin',
               'underlying_isin', 'currency', 'product_type', 'extended_product_type',
               'margin_style_flag', 'exercise_style_flag', 'product_settlement_type',
               'final_settlement_time', 'product_tick_size', 'product_tick_value',
               'liquidation_group', 'xm_eligibility']


class ProductsRequestHandler(RequestHandler):
    """Handler for sending requests to the /products endpoint and exporting data."""

    def __init__(self,
                 date=None,
                 version=None,
                 to_excel=False,
                 to_json=False,
                 export_dir=None,
                 timestamp=None,
                 filters=None
                 ):
        super().__init__()
        self.business_date = self._get_business_date(date, version)
        self.version = version == "LIVE"
        self.to_excel = to_excel
        self.to_json = to_json
        self.export_dir = export_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.timestamp = timestamp if timestamp is not None else 0
        self.filter_handler = FilterHandler(EXTRAFIELDS, ["product_tick_size", "product_tick_value"])
        self.filters = self.filter_handler.parse_filters(filters)

    def process_and_provide_output(self) -> None:
        """Processes the data from /products and exports it according to the specified format."""
        products = self.send_request()

        filtered_products = self.filter_handler.filter_response(products, self.filters)

        DataExporter.export(filtered_products, "Products", self.export_dir, self.to_excel, self.to_json,
                            str(self.business_date), self.version)

    def send_request(self) -> List[Dict[str, Any]]:
        """Sends a GET request to /products endpoint with optional filters, date, and version."""
        try:
            response = self.api.products_get(extrafields=EXTRAFIELDS,
                                             business_date=self.business_date,
                                             live_timestamp=self.timestamp,
                                             live=self.version)
            self._check_for_error_in_response(response)
            response = response.get("products", [])
            return response
        except Exception as e:
            self._handle_request_error(e)
        return []
