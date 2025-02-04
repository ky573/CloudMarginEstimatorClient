"""
This module contains logic for retrieving data about series and giving
output to the user.
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

EXTRAFIELDS = ['product_id', 'contract_date', 'contract_maturity', 'expiry_maturity',
               'call_put_flag', 'exercise_price', 'version_number', 'iid',
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
                 call_put_flag=None,
                 filters=None,
                 template=False
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
        self.call_put_flag = call_put_flag
        self.filters = self._parse_filters(filters)
        self.template = template

    def process_and_provide_output(self) -> None:
        """Processes the data from /series and exports it according to the specified format."""
        series = self.send_request()

        filtered_series = self._filter_response(series)

        context = ExportContext()

        file_suffix = "series"

        if self.to_excel:
            context.set_strategy(ExcelExportStrategy(file_suffix))
        elif self.to_json:
            context.set_strategy(JSONExportStrategy(file_suffix))
        else:
            context.set_strategy(CSVExportStrategy(file_suffix))

        context.export_data(str(self.business_date), self.version, filtered_series, self.export_dir)

        click.echo(f"Series exported to {self.export_dir}")

        if self.template:
            self._generate_etd_portfolio_template(filtered_series)

    def send_request(self) -> List[Dict[str, Any]]:
        """Sends a GET request to the /series endpoint with optional filters, date, and version."""
        try:
            response = self.api.series_get(products=self.products,
                                           extrafields=EXTRAFIELDS,
                                           business_date=self.business_date,
                                           live_timestamp=self.timestamp,
                                           live=self.version)
            self._check_for_error_in_response(response)
            print(json.dumps(response, indent=4))
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

        context = ExportContext()

        if self.to_excel:
            context.set_strategy(ExcelExportStrategy("etd_portfolio_template"))
        else:
            context.set_strategy(CSVExportStrategy("etd_portfolio_template"))

        context.export_data(str(self.business_date), self.version, etd_portfolio, self.export_dir)
        click.echo(f"ETD portfolio template exported to {self.export_dir}")

    def _parse_filters(self, filter_str: Optional[str]) -> Dict[str, Union[str, int]]:
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

                    if key in INT_VALUES:
                        try:
                            filters[key] = int(value)
                        except ValueError:
                            raise ValueError(f"Invalid integer value for {key}: {value}")
                    else:
                        filters[key] = value

            except ValueError as e:
                click.echo(str(e))
                raise click.Abort()
        return filters

    def _filter_response(self, series: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filters series based on extrafields values defined in self.filters."""
        filtered_series = []

        for series_ in series:
            if self.call_put_flag:
                if self.call_put_flag == "C" and series_.get("call_put_flag") != "C":
                    continue
                elif self.call_put_flag == "P" and series_.get("call_put_flag") != "P":
                    continue

            match = True
            for key, value in self.filters.items():
                if series_.get(key) != value:
                    match = False
                    break

            if match:
                filtered_series.append(series_)

        return filtered_series
