from typing import List, Dict, Any


class Extractor:
    """Class to extract data from a response."""

    INITIAL_MARGIN_INDEX = 0  # Index of the initial margin in the portfolio margin list

    def __init__(self):
        self.initial_margins: List[float] = []
        self.dates: List[int] = []

    def extract_data(self, data: Dict[str, Any]) -> None:
        """Extracts and aggregates initial margin data from the API response."""
        business_date = int(data['business_date'])
        initial_margin = data['portfolio_margin'][self.INITIAL_MARGIN_INDEX]['initial_margin']

        self.dates.append(business_date)
        self.initial_margins.append(float(initial_margin))
