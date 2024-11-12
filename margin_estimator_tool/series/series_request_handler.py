from datetime import datetime
from typing import Dict, Any, Optional, List
import click
import os
from margin_estimator_tool.export_strategy.export_context import ExportContext
from margin_estimator_tool.export_strategy.csv_export_strategy import CSVExportStrategy
from margin_estimator_tool.export_strategy.excel_export_strategy import ExcelExportStrategy
from margin_estimator_tool.export_strategy.json_export_strategy import JSONExportStrategy
from margin_estimator_tool.core.request_handler_base import RequestHandler


class SeriesRequestHandler(RequestHandler):
    """Handler for sending requests to the /series endpoint and exporting data."""

    def __init__(self, date=None, version=None, timestamp=None, to_excel=False, export_dir=None, to_json=False, products=None, type=None, filters=None):
        super().__init__()
        self.business_date = int(date) if date is not None else datetime.today().strftime('%Y%m%d')
        self.version = version == "LIVE"
        self.timestamp = timestamp
        self.to_excel = to_excel
        self.to_json = to_json
        self.export_dir = export_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.products = products
        self.type = type
        self.filters = self._parse_filters(filters)

    def process_and_export(self) -> None:
        """Processes the data from /series and exports it according to the specified format."""


    def send_request(self) -> List[Dict[str, Any]]:
        """Sends a GET request to the /series endpoint with optional filters, date, and version."""
