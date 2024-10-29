import json
from typing import Dict, Any, Optional, List
from margin_estimator_tool.margin_calculator.export_strategy.export_context import ExportContext
from margin_estimator_tool.margin_calculator.export_strategy.csv_export_strategy import CSVExportStrategy
from margin_estimator_tool.margin_calculator.export_strategy.excel_export_strategy import ExcelExportStrategy
from margin_estimator_tool.margin_calculator.export_strategy.json_export_strategy import JSONExportStrategy
from .request_handler_base import RequestHandler
import requests
import click

EXTRAFIELDS = ['product', 'instrument_type', 'clearing_house', 'prod_name', 'prod_isin',
               'underlying_isin', 'currency', 'product_type', 'extended_product_type',
               'margin_style_flag', 'exercise_style_flag', 'product_settlement_type',
               'final_settlement_time', 'product_tick_size', 'product_tick_value',
               'liquidation_group', 'xm_eligibility']


class ProductsRequestHandler(RequestHandler):
    """Handler for sending requests to the /products endpoint and exporting data."""

    def __init__(self, date: Optional[str], version: Optional[str], filters: Optional[str], to_excel: bool,
                 to_json: bool, export_dir: str):
        super().__init__()
        self.date = date
        self.version = self._parse_version(version)
        self.filters = self._parse_filters(filters)
        self.to_excel = to_excel
        self.to_json = to_json
        self.export_dir = export_dir

    def _parse_filters(self, filter_str: Optional[str]) -> Dict[str, str]:
        """Parses the filter string into a dictionary."""
        if filter_str:
            return dict(f.split(':') for f in filter_str.split(','))
        return {}

    def _parse_version(self, version: str) -> bool:
        """Parses the version from CLI"""
        if version == "SOD":
            return False
        else:
            return True

    def _filter_response(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters products based on extrafields values defined in self.filters."""
        filtered_products = []

        for product in products:
            if product.get("instrument_type") == "future":
                filtered_products.append(product)

        return filtered_products

    def send_request(self) -> List[Dict[str, Any]]:
        """Sends a GET request to the /products endpoint with optional filters, date, and version."""
        extrafields = list(self.filters.keys())
        business_day = int(self.date)

        try:
            response = self.api.products_get(extrafields=extrafields, business_day=business_day, live=self.version)
            response = response.get("products", [])
            return response
        except requests.exceptions.HTTPError as e:
            click.echo(f"HTTP Error: {e}", err=True)
        except requests.exceptions.RequestException as e:
            click.echo(f"Error sending request: {e}", err=True)
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
        return []

    def process_and_export(self) -> None:
        """Processes the data from /products and exports it according to the specified format."""
        products = self.send_request()

        filtered_products = self._filter_response(products)
        print(filtered_products)

        context = ExportContext()

        if self.to_excel:
            context.set_strategy(ExcelExportStrategy())
        elif self.to_json:
            context.set_strategy(JSONExportStrategy())
        else:
            context.set_strategy(CSVExportStrategy())

        context.export_data(filtered_products, self.export_dir)
