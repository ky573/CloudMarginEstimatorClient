"""
This module contains logic for retrieving data about series and giving
output to the user.
"""


import json
from datetime import datetime
from typing import Dict, Any, Optional, List, Union
import os
import click
from margin_estimator_tool.export_strategy.export_context import ExportContext
from margin_estimator_tool.export_strategy.csv_export_strategy import CSVExportStrategy
from margin_estimator_tool.export_strategy.excel_export_strategy import ExcelExportStrategy
from margin_estimator_tool.export_strategy.json_export_strategy import JSONExportStrategy
from margin_estimator_tool.core.request_handler_base import RequestHandler

EXTRAFIELDS = ['product_id', 'contract_date', 'contract_maturity', 'expiry_maturity',
               'call_put_flag', 'exercies_price', 'version_number', 'iid',
               'act_trade_unit_no', 'days_to_expiration', 'trade_unit_value',
               'exercise_style_flag', 'contract_frequency']

INT_VALUES = ['contract_date', 'contract_maturity', 'expiry_maturity',
              'exercise_price', 'iid', 'act_trade_unit_no',
              'days_to_expiration', 'trade_unit_value']


class SeriesRequestHandler(RequestHandler):
    """Handler for sending requests to the /series endpoint and exporting data."""

    def __init__(self,
                 date=None,
                 version=None,
                 timestamp=None,
                 to_excel=False,
                 export_dir=None,
                 to_json=False,
                 products=None,
                 type=None,
                 filters=None
                 ):
        super().__init__()
        self.business_date = self._get_business_date(date, version)
        self.version = version == "LIVE"
        self.timestamp = timestamp if timestamp is not None else 0
        self.to_excel = to_excel
        self.to_json = to_json
        self.export_dir = export_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.products = products.split(',')
        self.type = type
        self.filters = self._parse_filters(filters)

    def process_and_provide_output(self) -> None:
        """Processes the data from /series and exports it according to the specified format."""
        series = self.send_request()

        filtered_series = self._filter_response(series)

        context = ExportContext()

        if self.to_excel:
            context.set_strategy(ExcelExportStrategy("series"))
        elif self.to_json:
            context.set_strategy(JSONExportStrategy("series"))
        else:
            context.set_strategy(CSVExportStrategy("series"))

        context.export_data(str(self.business_date), self.version, filtered_series, self.export_dir)

        click.echo(f"Series exported to {self.export_dir}")

    def send_request(self) -> List[Dict[str, Any]]:
        """Sends a GET request to the /series endpoint with optional filters, date, and version."""
        try:
            response = self.api.series_get(products=self.products,
                                           extrafields=EXTRAFIELDS,
                                           business_date=self.business_date,
                                           live_timestamp=self.timestamp,
                                           live=self.version)
            print(json.dumps(response, indent=4))
            response = response.get("list_series", [])
            click.echo("Request sent successfully.")
            return response
        except Exception as e:
            self._handle_request_error(e)
        return []

    def _parse_filters(self, filter_str: Optional[str]) -> Dict[str, Union[str, int]]:
        """Parses the filter string into a dictionary."""
        filters: Dict[str, Union[str, int]] = {}
        if filter_str:
            for f in filter_str.split(','):
                key, value = f.split(':')

                if key not in EXTRAFIELDS:
                    click.echo("No such extrafield")
                    continue

                if key in INT_VALUES:
                    filters[key] = int(value)
                else:
                    filters[key] = value

        return filters

    def _filter_response(self, series: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters series based on extrafields values defined in self.filters."""
        filtered_series = []

        for series_ in series:
            match = True
            for key, value in self.filters.items():
                if series_.get(key) != value:
                    match = False
                    break

            if match:
                filtered_series.append(series_)

        return filtered_series
