from margin_estimator_tool.core.request_handler_base import RequestHandler
from datetime import datetime
import click
from typing import Optional, List, Dict, Any


class SnapshotRequestHandler(RequestHandler):
    """Handles fetching and displaying SOD snapshots (non-live)."""

    def __init__(self, date_from: str, date_to: Optional[str] = None):
        super().__init__()
        self.date_from = date_from
        self.date_to = date_to or datetime.now().strftime("%Y%m%d")

    def process_and_provide_output(self) -> None:
        """Processes the data from /snapshots and outputs it according to the specified format."""
        snapshots = self.send_request()

        filtered_snapshots = [snap for snap in snapshots if not snap.get("live", True)]

        self._print_output(filtered_snapshots)

    def send_request(self) -> List[Dict[str, Any]]:
        """Sends a GET request to the /snapshots endpoint."""
        try:
            response = self.api.snapshots_get(business_date_from=self.date_from, business_date_to=self.date_to)
            response = response.get("snapshots", [])
            return response
        except Exception as e:
            self._handle_request_error(e)
        return []

    def _print_output(self, filtered_snapshots):
        """Prints the output in desired format."""
        for idx, snapshot in enumerate(filtered_snapshots, start=1):
            date = snapshot.get('business_date')
            otc = "YES" if snapshot.get('otc_available', 'N/A') is True else "NO"
            cash = "YES" if snapshot.get('cash_available', 'N/A') is True else "NO"
            click.echo(f"  [{idx:02d}] date: {date} OTC={otc}, CASH={cash}")
