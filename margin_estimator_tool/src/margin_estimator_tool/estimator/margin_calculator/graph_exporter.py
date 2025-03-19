"""Module to handle exporting margin details as a graph."""

from typing import List
from datetime import datetime
import plotly.graph_objects as go  # type: ignore


class GraphExporter:
    """Class to handle exporting the initial margin graph."""

    def __init__(
        self, dates: List[int], initial_margins: List[float], export_dir: str
    ) -> None:
        """
        Initializes the GraphExporter instance.

        Args:
            dates: list of dates for x-axis
            initial_margins: list of initial margins for y-axis
            export_dir: directory to export to
        """
        self.dates = dates
        self.initial_margins = initial_margins
        self.export_dir = export_dir

    def save_graph(self) -> None:
        """Saves the initial margin graph to a file."""
        fig = self._plot_graph()

        fig.write_image(f"{self.export_dir}/initial_margin_graph.jpeg")

    def _plot_graph(self) -> go.Figure:
        """Plots the initial margin graph."""
        formatted_dates = [
            datetime.strptime(str(date), "%Y%m%d") for date in self.dates
        ]

        fig = go.Figure(
            data=go.Scatter(
                x=formatted_dates, y=self.initial_margins, mode="lines+markers"
            )
        )
        fig.update_layout(
            title="Initial Margin Over Time",
            xaxis_title="Date",
            yaxis_title="Initial Margin (EUR)",
            xaxis={"tickformat": "%Y-%m-%d", "type": "date"},
        )

        return fig
