"""
Class to handle filter parsing for products and series endpoint.
"""


from typing import Dict, Any, Optional, List, Union, Callable
import click


class FilterHandler:
    """Handles parsing and applying filters to a dataset."""

    def __init__(self, extrafields: List[str], int_values: Optional[List[str]] = None):
        """
        Initializes the FilterHandler instance.

        Args:
            extrafields: extrafields to be checked in parsing
            int_values: values from extrafields to be converted to int
        """
        self.extrafields = set(extrafields)
        self.int_values = set(int_values) if int_values else set()

    def parse_filters(self, filter_str: Optional[str]) -> Dict[str, Union[str, int, bool]]:
        """
        Parses a filter string into a dictionary to be later used for
        filtering of the response. Correct types are assigned to values.

        If format is malformed (i.e., not a key:value pair), or one of the
        keys is not in extrafields, or it contains a wrong type, exception is thrown.

        Args:
            filter_str: string to be parsed.

        Returns:
            A dictionary containing correct key:value pairs in proper type mapping
        """
        filters: Dict[str, Union[str, int, bool]] = {}
        if not filter_str:
            return filters

        try:
            for f in filter_str.split(','):
                parts = f.split(':', 1)
                if len(parts) != 2:
                    raise ValueError(f"Invalid filter format: {f}. Expected 'key:value'")

                key, value = parts

                if key not in self.extrafields:
                    raise ValueError(f"Invalid filter key: {key}. Must be one of {self.extrafields}")

                if key in self.int_values:
                    try:
                        filters[key] = int(value)
                    except ValueError:
                        raise ValueError(f"Invalid integer value for {key}: {value}")
                elif key == "xm_eligibility":
                    filters[key] = False if value.lower() == "false" else True
                else:
                    filters[key] = value

        except ValueError as e:
            raise click.ClickException(str(e))

        return filters

    @staticmethod
    def filter_response(data: List[Dict[str, Any]],
                        filters: Dict[str, Union[str, int, bool]],
                        custom_filters: Optional[Dict[str, Callable[[Dict[str, Any]], bool]]] = None
                        ) -> List[Dict[str, Any]]:
        """
        Filters a list of dictionaries based on the given filters.
        Custom filters in form of callables can also be applied.

        Args:
            data: data from request to be filtered
            filters: dictionary of key:value pairs to be used for filtering
            custom_filters: additional custom filters in form of functions

        Returns:
            A list of filtered data
        """
        custom_filters = custom_filters or {}

        filtered_data = []
        for item in data:
            if any(item.get(key) != value for key, value in filters.items()):
                continue

            if any(not func(item) for func in custom_filters.values()):
                continue

            filtered_data.append(item)

        return filtered_data
