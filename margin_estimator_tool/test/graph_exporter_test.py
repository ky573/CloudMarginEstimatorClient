import pytest
import plotly.graph_objects as go
from datetime import datetime
from unittest.mock import patch, MagicMock
from margin_estimator_tool.src.margin_estimator_tool.estimator.margin_calculator.graph_exporter import GraphExporter


class TestGraphExporter:
    """Test suite for the GraphExporter class."""

    def setup_method(self):
        """Setup test data before each test."""
        self.dates = [20240318, 20240319, 20240320]
        self.initial_margins = [1500.75, 1600.50, 1700.25]
        self.export_dir = "test_dir"
        self.exporter = GraphExporter(self.dates, self.initial_margins, self.export_dir)

    def test_initialization(self):
        """Tests that the exporter is initialized correctly."""
        assert self.exporter.dates == self.dates
        assert self.exporter.initial_margins == self.initial_margins
        assert self.exporter.export_dir == self.export_dir

    def test_plot_graph(self):
        """Tests that the _plot_graph method generates a valid Plotly figure."""
        fig = self.exporter._plot_graph()
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1  # Only one trace should be present
        assert fig.data[0].x == tuple([datetime.strptime(str(d), "%Y%m%d") for d in self.dates]) # Expects a tuple
        assert fig.data[0].y == tuple(self.initial_margins) # Expects a tuple

    @patch("plotly.graph_objects.Figure.write_image")
    def test_save_graph(self, mock_write_image):
        """Tests that save_graph calls the write_image method correctly."""
        self.exporter.save_graph()
        mock_write_image.assert_called_once_with(f"{self.export_dir}/initial_margin_graph.jpeg")