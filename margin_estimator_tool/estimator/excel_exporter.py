"""Module to handle exporting margin details to an Excel file."""

from typing import List, Dict, Union, Tuple, Set
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from margin_estimator_tool.core.utils import flatten_dict


class ExcelExporter:
    """Class to handle exporting margin details to an Excel file."""

    def __init__(self, margin_details: List[Dict[str, Union[List, Dict]]], export_dir: str):
        self.margin_details = margin_details
        self.export_dir = export_dir
        self.wb = Workbook()

    def export_to_excel(self) -> None:
        """Exports margin details to an Excel file."""
        ws1 = self._create_and_title_sheet("portfolio_margin")
        ws2 = self._create_and_title_sheet("drilldowns")

        portfolio_headers, drilldown_headers = self._prepare_headers()

        self._populate_sheet(ws1, portfolio_headers, "portfolio_margin")
        self._populate_sheet(ws2, drilldown_headers, "drilldowns")

        self._save_workbook("margin_details.xlsx")

    def _create_and_title_sheet(self, title: str) -> Worksheet:
        """Creates a new sheet in the workbook with the given title."""
        ws = self.wb.create_sheet(title=title)
        return ws

    def _save_workbook(self, filename: str) -> None:
        """Saves the workbook to the specified directory with the given filename."""
        self.wb.save(f"{self.export_dir}/{filename}")
        print(f"Excel file saved to {self.export_dir}/{filename}")

    def _prepare_headers(self) -> Tuple[List[str], List[str]]:
        """Prepares headers for portfolio and drilldowns sheets."""
        portfolio_headers = self._extract_headers("portfolio_margin")
        drilldown_headers = self._extract_headers("drilldowns")
        return portfolio_headers, drilldown_headers

    def _extract_headers(self, key: str) -> List[str]:
        """Extracts headers by examining all data entries for the given key."""
        headers: Set[str] = set()
        for detail in self.margin_details:
            for item in detail[key]:
                flat_item = flatten_dict(item)
                headers.update(flat_item.keys())
        headers_list = ['business_date'] + sorted(list(headers))
        return headers_list

    def _populate_sheet(self, ws: Worksheet, headers: List[str], data_key: str) -> None:
        """Populates a given worksheet with data based on the specified headers."""
        ws.append(headers)
        self._append_data_to_sheet(ws, headers, data_key)

    def _append_data_to_sheet(self, ws: Worksheet, headers: List[str], data_key: str) -> None:
        """Appends data to the worksheet based on the specified headers and data key."""
        for detail in self.margin_details:
            business_date = detail["business_date"]
            for item in detail[data_key]:
                flat_item = flatten_dict(item)
                row = [business_date] + [flat_item.get(header, '') for header in headers[1:]]
                ws.append(row)
