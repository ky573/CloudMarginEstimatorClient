"""This module contains class to extract data from response sent back from estimator."""


from typing import List, Dict, Any


class Extractor:
    """Class to extract data from a response."""

    INITIAL_MARGIN_INDEX = 0  # Index of the initial margin in the portfolio margin list

    def __init__(self):
        self._initial_margins: List[float] = []
        self._dates: List[int] = []

    def extract_data(self, data: Dict[str, Any]) -> None:
        """
        Extracts and aggregates initial margin data from the API response.

        Args:
            data: data returned from the endpoint in form of a dictionary
        """
        business_date = int(data["business_date"])
        initial_margin = data["portfolio_margin"][self.INITIAL_MARGIN_INDEX]["initial_margin"]

        self._dates.append(business_date)
        self._initial_margins.append(float(initial_margin))

    @property
    def initial_margins(self) -> List[float]:
        """Returns the list of extracted initial margins."""
        return self._initial_margins

    @property
    def dates(self) -> List[int]:
        """Returns the list of extracted business dates."""
        return self._dates
