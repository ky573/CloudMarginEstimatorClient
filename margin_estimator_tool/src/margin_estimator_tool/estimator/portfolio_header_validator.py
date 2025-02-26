"""This module contains logic for header validation of etd portfolios."""


import csv
import click
from typing import Tuple


class HeaderValidator:
    """Class to validate CSV headers for portfolio files."""

    GUI_HEADER = "Product ID,Contract Date,Call Put Flag,Exercise Price,Version Number,Net LS Balance"
    INNER_HEADER = "call_put_flag,component_margin,component_margin_currency,contract_date,exercise_price,exercise_style,iid,instrument_type,line_no,liquidation_group,liquidation_group_split,maturity,net_ls_balance,premium_margin,premium_margin_currency,product_id,version_number"

    def __init__(self) -> None:
        """Initialize the HeaderValidator with default values."""
        self.is_gui_format: bool = False
        self.is_inner_format: bool = False

    def validate_headers(self, csv_file: str) -> bool:
        """
        Validates the CSV file headers against the required formats.

        Args:
            csv_file: Path to the CSV file to validate

        Returns:
            True if headers are valid, False otherwise
        """
        try:
            with open(csv_file, mode='r', newline='', encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader, None)
                if headers is None:
                    raise ValueError("CSV file is empty.")

                headers_str = ",".join(headers)
                if headers_str == self.GUI_HEADER:
                    self.is_gui_format = True
                elif headers_str == self.INNER_HEADER:
                    self.is_inner_format = True

                if not self.is_gui_format and not self.is_inner_format:
                    raise ValueError(f"Headers mismatch. Expected: either '{self.GUI_HEADER}' "
                                     f"or '{self.INNER_HEADER}', Found: '{headers_str}'.")

            click.echo("Headers validated successfully.")
            return True
        except (ValueError, FileNotFoundError) as e:
            click.echo(f"Error validating CSV headers: {e}")
            return False

    def get_header_format(self) -> Tuple[bool, bool]:
        """
        Returns the detected header format after validation.

        Returns:
            Tuple (is_gui_format, is_inner_format)
        """
        return self.is_gui_format, self.is_inner_format
