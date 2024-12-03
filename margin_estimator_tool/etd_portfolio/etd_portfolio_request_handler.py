"""
This module contains logic for retrieving information about products from
endpoint and then outputting them in desired form.
"""


from typing import Dict, Any, Optional, List, Union
import os
import click
from margin_estimator_tool.export_strategy.export_context import ExportContext
from margin_estimator_tool.export_strategy.csv_export_strategy import CSVExportStrategy
from margin_estimator_tool.export_strategy.excel_export_strategy import ExcelExportStrategy
from margin_estimator_tool.export_strategy.json_export_strategy import JSONExportStrategy
from margin_estimator_tool.core.request_handler_base import RequestHandler


class EtdPortfolioRequestHandler(RequestHandler):
    """Handler for sending requests to the /products endpoint and exporting data."""

    def __init__(self,
                 csv_file,
                 date=None,
                 version=None,
                 timestamp=None,
                 to_excel=False,
                 to_json=False,
                 export_dir=None,
                 ):
        super().__init__()
        self.csv_file = csv_file
        self.business_date = self._get_business_date(date, version)
        self.version = version == "LIVE"
        self.timestamp = timestamp
        self.to_excel = to_excel
        self.to_json = to_json
        self.export_dir = export_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    def process_and_provide_output(self) -> None:
        """Processes the data from /estimator and exports it according to the specified format."""

        click.echo(f"Portfolio exported to {self.export_dir}")

    def send_request(self) -> List[Dict[str, Any]]:
        """Sends a POST request to /estimator endpoint with provided portfolio."""
