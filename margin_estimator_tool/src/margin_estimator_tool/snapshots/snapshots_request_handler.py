"""
This module contains logic for retrieving information about currently
available snapshots for range of dates and then outputs it.
"""


from datetime import datetime
from typing import Optional, List, Dict, Any
import click
from margin_estimator_tool.src.margin_estimator_tool.core.request_handler_base import RequestHandler


class SnapshotRequestHandler(RequestHandler):
    """Handles fetching and displaying SOD snapshots (non-live)."""

    def __init__(self, date_from: str, date_to: Optional[str] = None) -> None:
        """
        Initilizes a new SnapshotRequestHandler instance. If date_to is greater than
        date_from, no data will be returned back.
        
        Args:
            date_from: Starting date for the range, must be specified.
            date_to: End date of the range, optional, defaults to current date.
        """
        super().__init__()
        self.date_from = date_from
        self.date_to = date_to or datetime.now().strftime("%Y%m%d")

    def process_and_provide_output(self) -> None:
        """Processes the data from /snapshots and outputs it according to the specified format."""
        snapshots = self.send_request()
        filtered_snapshots = [snap for snap in snapshots if not snap.get("live", True)]
        self._print_output(filtered_snapshots)

    def send_request(self) -> List[Dict[str, Any]]:
        """
        Sends a GET request to the /snapshots endpoint.
        It also checks for the error in the response.

        Returns:
            response: Response returned from the endpoint containing data about snapshots.
                      Returns empty list in case of an error during the request.
        """
        try:
            response = self.api.snapshots_get(business_date_from=self.date_from,
                                              business_date_to=self.date_to)
            self._check_for_error_in_response(response)
            response = response.get("snapshots", [])
            return response
        except Exception as e:
            self._handle_request_error(e)
        return []

    @staticmethod
    def _print_output(filtered_snapshots):
        """Prints the output in desired format."""
        for idx, snapshot in enumerate(filtered_snapshots, start=1):
            date = snapshot.get("business_date")
            otc = "YES" if snapshot.get("otc_available", "N/A") is True else "NO"
            cash = "YES" if snapshot.get("cash_available", "N/A") is True else "NO"
            click.echo(f"  [{idx:02d}] date: {date} OTC={otc}, CASH={cash}")
