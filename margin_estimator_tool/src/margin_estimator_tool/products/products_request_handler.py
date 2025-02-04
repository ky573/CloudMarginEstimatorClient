"""
This module contains logic for retrieving information about products from
endpoint and then outputting them in desired form.
"""
import json
from typing import Dict, Any, Optional, List, Union
import os
import click
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.export_context import ExportContext
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.csv_export_strategy import CSVExportStrategy
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.excel_export_strategy import ExcelExportStrategy
from margin_estimator_tool.src.margin_estimator_tool.export_strategy.json_export_strategy import JSONExportStrategy
from margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base import RequestHandler


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
        self.filters = self._parse_filters(filters)

    def process_and_provide_output(self) -> None:
        """Processes the data from /products and exports it according to the specified format."""
        products = self.send_request()

        filtered_products = self._filter_response(products)

        context = ExportContext()

        file_suffix = "products"

        if self.to_excel:
            context.set_strategy(ExcelExportStrategy(file_suffix))
        elif self.to_json:
            context.set_strategy(JSONExportStrategy(file_suffix))
        else:
            context.set_strategy(CSVExportStrategy(file_suffix))

        context.export_data(str(self.business_date),
                            self.version,
                            filtered_products,
                            self.export_dir)

        click.echo(f"Products exported to {self.export_dir}")

    def send_request(self) -> List[Dict[str, Any]]:
        """Sends a GET request to /products endpoint with optional filters, date, and version."""
        try:
            response = self.api.products_get(extrafields=EXTRAFIELDS,
                                             business_date=self.business_date,
                                             live_timestamp=self.timestamp,
                                             live=self.version)
            print(json.dumps(response, indent=4))
            self._check_for_error_in_response(response)
            response = response.get("products", [])
            return response
        except Exception as e:
            self._handle_request_error(e)
        return []

    def _parse_filters(self, filter_str: Optional[str]) -> Dict[str, Union[str | int]]:
        """Parses the filter string into a dictionary."""
        filters: Dict[str, Union[str, int]] = {}
        if filter_str:
            try:
                for f in filter_str.split(','):
                    parts = f.split(':', 1)

                    if len(parts) != 2:
                        raise ValueError(f"Invalid filter format: {f}. Expected 'key:value'")

                    key, value = parts

                    if key not in EXTRAFIELDS:
                        raise ValueError(f"Invalid filter key: {key}. Must be one of {EXTRAFIELDS}")

                    if key in ("product_tick_size", "product_tick_value"):
                        try:
                            filters[key] = int(value)
                        except ValueError:
                            raise ValueError(f"Invalid integer value for {key}: {value}")
                    elif key == "xm_eligibility":
                        filters[key] = False if value.lower() == "false" else True
                    else:
                        filters[key] = value

            except ValueError as e:
                click.echo(str(e))
                raise click.Abort()

        return filters

    def _filter_response(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters products based on extrafields values defined in self.filters."""
        filtered_products = []

        for product in products:
            match = True
            for key, value in self.filters.items():
                if product.get(key) != value:
                    match = False
                    break

            if match:
                filtered_products.append(product)

        return filtered_products
