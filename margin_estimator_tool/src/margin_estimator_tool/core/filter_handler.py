"""
Module to handle filter parsing for products and series endpoint.
"""

from typing import Dict, Any, Optional, List, Union, Callable
import click


class FilterHandler:
    """Handles parsing and applying filters to a dataset."""

    def __init__(
        self, extrafields: List[str], numeric_values: Optional[List[str]] = None
    ) -> None:
        """
        Initializes the FilterHandler instance.

        Args:
            extrafields: extrafields to be checked in parsing
            numeric_values: values from extrafields to be converted to int or float
        """
        self.extrafields = set(extrafields)
        self.numeric_values = set(numeric_values) if numeric_values else set()

    def parse_filters(
        self, filter_str: Optional[str]
    ) -> Dict[str, Union[str, int, float, bool]]:
        """
        Parses a filter string into a dictionary with correctly typed values.

        Args:
            filter_str: string to be parsed.

        Returns:
            A dictionary containing key-value pairs with appropriate types.
        """
        filters = {}
        if not filter_str:
            return filters

        for f in filter_str.split(","):
            key, value = self._parse_key_value_pair(f)
            self._validate_key(key)
            filters[key] = self._parse_value(key, value)

        return filters

    @staticmethod
    def _parse_key_value_pair(filter_item: str) -> tuple[str, str]:
        """Splits a filter item into a key-value pair and checks for correct format."""
        parts = filter_item.split(":", 1)
        if len(parts) != 2:
            raise click.ClickException(
                f"Invalid filter format: {filter_item}. Expected 'key:value'"
            )
        return parts[0], parts[1]

    def _validate_key(self, key: str) -> None:
        """Checks if the key is in the allowed extrafields."""
        if key not in self.extrafields:
            raise click.ClickException(
                f"Invalid filter key: {key}. Must be one of {self.extrafields}"
            )

    def _parse_value(self, key: str, value: str) -> Union[str, int, float, bool]:
        """Parses the value into the appropriate type based on the key."""
        if key in self.numeric_values:
            return self._parse_numeric_value(key, value)
        if key == "xm_eligibility":
            return self._parse_boolean_value(value)
        return value

    @staticmethod
    def _parse_numeric_value(key: str, value: str) -> Union[int, float]:
        """Attempts to parse a value as a float or integer."""
        try:
            return float(value) if "." in value else int(value)
        except ValueError:
            raise click.ClickException(f"Invalid numeric value for {key}: {value}")

    @staticmethod
    def _parse_boolean_value(value: str) -> bool:
        """Parses a value as a boolean, assuming specific strings map to False."""
        return value.lower() != "false"

    @staticmethod
    def filter_response(
        data: List[Dict[str, Any]],
        filters: Dict[str, Union[str, int, bool]],
        custom_filters: Optional[Dict[str, Callable[[Dict[str, Any]], bool]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Filters a list of dictionaries based on the given filters.
        Custom filters in form of callables can also be applied.

        Args:
            data: data from request to be filtered
            filters: dictionary of key and value pairs to be used for filtering
            custom_filters: additional custom filters in form of functions

        Returns:
            A list of filtered data
        """
        custom_filters = custom_filters or {}
        filtered_data = []

        for item in data:
            if any(item.get(key) != value for key, value in filters.items()) or any(
                not func(item) for func in custom_filters.values()
            ):
                continue
            filtered_data.append(item)

        click.echo(f"Filtered down to {len(filtered_data)} items.")
        return filtered_data
