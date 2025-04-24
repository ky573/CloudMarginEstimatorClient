"""
This module is responsible for retrieving the information about
live snapshots from estimator. It prints out the information
in formatted output.
"""

from datetime import datetime
from typing import Dict, Any, List
import click
from core.request_handler_base import RequestHandler


class LiveSnapshotRequestHandler(RequestHandler):
    """Handler for sending requests to the /live_snapshot endpoint."""

    def __init__(self, date: str):
        """
        Initializes the LiveSnapshotsRequestHandler instance

        Args:
            date: desired date
        """
        super().__init__()
        self._business_date = int(date)

    def process_and_provide_output(self) -> None:
        """Processes the data from /live_snapshots and outputs it according to specified format."""
        live_snapshots = self.send_request()
        self._print_output(live_snapshots)

    def send_request(self) -> List[Dict[str, Any]]:
        """
        Sends a GET request to the /live_snapshots endpoint.
        It also checks for erros in the response.

        Returns:
            response: list of data from the live_snapshots endpoint.
                      Returns an empty list in case of an error in the request.
        """
        try:
            response = self._api.live_snapshots_get(business_date=self._business_date)
            self._check_for_error_in_response(response)
            response = response.get("snapshots", [])
            return response
        except Exception as e:
            self._handle_request_error(e)
        return []

    def _print_output(self, live_snapshots: List[Dict[str, Any]]) -> None:
        """Prints the output in desired format."""
        click.echo(f"Available live snapshots for {self._business_date}:")
        for idx, snapshot in enumerate(live_snapshots, start=1):
            timestamp = snapshot.get("live_timestamp", "N/A")
            time = (
                datetime.fromtimestamp(int(timestamp) / 1000).strftime("%H:%M:%S")
                if timestamp != 0
                else 0
            )
            otc = "YES" if snapshot.get("otc_available", "N/A") is True else "NO"
            cash = "YES" if snapshot.get("cash_available", "N/A") is True else "NO"
            click.echo(
                f"  [{idx:02d}] time: {time} ts:{timestamp} OTC={otc}, CASH={cash}"
            )
