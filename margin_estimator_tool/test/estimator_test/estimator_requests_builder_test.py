"""Test suite for EstimatorRequestBuilder class."""

import pytest
from unittest.mock import patch, mock_open, MagicMock
from io import StringIO
from margin_estimator_tool.src.margin_estimator_tool.estimator.portfolio_header_validator import (
    HeaderValidator,
)
from margin_estimator_tool.src.margin_estimator_tool.estimator.estimator_request_builder import (
    EstimatorRequestBuilder,
)


class TestEstimatorRequestBuilder:
    """Test cases for EstimatorRequestBuilder class."""

    @pytest.fixture
    def header_validator_mock(self):
        return MagicMock(spec=HeaderValidator)

    @pytest.fixture
    def builder(self, header_validator_mock):
        return EstimatorRequestBuilder(header_validator_mock)

    def test_initialization(self, header_validator_mock):
        """Test if the EstimatorRequestBuilder initializes correctly."""
        builder = EstimatorRequestBuilder(header_validator_mock)
        assert builder.header_validator == header_validator_mock

    @patch("cpme_api.models.BodyEstimator")
    @patch("cpme_api.models.Snapshot")
    @patch("cpme_api.models.BodyEstimatorPortfolioComponents")
    @patch("cpme_api.models.EtdCsv")
    @patch("builtins.open", new_callable=mock_open, read_data="mock_csv_content")
    def test_build_gui_format_request(
        self,
        mock_file,
        mock_etd_csv,
        mock_components,
        mock_snapshot,
        mock_body_estimator,
        builder,
    ):
        """Test if _build_gui_format_request correctly builds a GUI format request."""
        # Setup mocks
        mock_body_instance = MagicMock()
        mock_snapshot_instance = MagicMock()
        mock_components_instance = MagicMock()
        mock_etd_csv_instance = MagicMock()

        mock_body_estimator.return_value = mock_body_instance
        mock_snapshot.return_value = mock_snapshot_instance
        mock_components.return_value = mock_components_instance
        mock_etd_csv.return_value = mock_etd_csv_instance

        mock_body_instance.snapshot = None
        mock_body_instance.portfolio_components = []

        # Setup test parameters
        business_day = 20250101
        csv_file = "test.csv"
        version = True
        timestamp = 1672531200

        # Create a patch for the _build_base_request method
        with patch.object(
            builder, "_build_base_request", return_value=mock_body_instance
        ) as mock_base_request:
            result = builder._build_gui_format_request(
                business_day, csv_file, version, timestamp
            )

            # Verify _build_base_request was called correctly
            mock_base_request.assert_called_once_with(business_day, version, timestamp)

            # Verify file was opened correctly
            mock_file.assert_called_once_with(csv_file, "r", encoding="utf-8")

            # Verify EtdCsv was created with correct CSV content
            mock_etd_csv.assert_called_once_with(csv="mock_csv_content")

            # Verify portfolio component was created and added to the request
            assert mock_components.called
            assert mock_components_instance in result.portfolio_components

    @patch("cpme_api.models.BodyEstimator")
    @patch("cpme_api.models.Snapshot")
    @patch("cpme_api.models.BodyEstimatorPortfolioComponents")
    @patch("cpme_api.models.EtdPositionsInner")
    @patch("builtins.open")
    def test_build_inner_format_request(
        self,
        mock_file,
        mock_etd_positions,
        mock_components,
        mock_snapshot,
        mock_body_estimator,
        builder,
    ):
        """Test if _build_inner_format_request correctly builds an inner format request."""
        # Setup mocks
        mock_body_instance = MagicMock()
        mock_snapshot_instance = MagicMock()
        mock_components_instance = MagicMock()
        mock_components_instance.etd_portfolio = []

        mock_body_estimator.return_value = mock_body_instance
        mock_snapshot.return_value = mock_snapshot_instance
        mock_components.return_value = mock_components_instance

        # Mock positions objects
        position1 = MagicMock()
        position2 = MagicMock()
        mock_etd_positions.side_effect = [position1, position2]

        mock_body_instance.snapshot = None
        mock_body_instance.portfolio_components = []

        # Mock CSV data
        csv_data = "header1,header2\nvalue1,value2\nvalue3,value4"
        mock_file.return_value = StringIO(csv_data)

        # Setup test parameters
        business_day = 20250101
        csv_file = "test.csv"
        version = True
        timestamp = 1672531200

        # Create a patch for the _build_base_request method
        with patch.object(
            builder, "_build_base_request", return_value=mock_body_instance
        ) as mock_base_request:
            result = builder._build_inner_format_request(
                business_day, csv_file, version, timestamp
            )

            # Verify _build_base_request was called correctly
            mock_base_request.assert_called_once_with(business_day, version, timestamp)

            # Verify portfolio component was created with correct type
            mock_components.assert_called_once_with(type="etd_portfolio")

            # Verify two positions were created and had attributes set
            assert mock_etd_positions.call_count == 2
            assert len(mock_components_instance.etd_portfolio) == 2

            # Verify attributes were set on position objects
            assert hasattr(position1, "_header1")
            assert hasattr(position1, "_header2")
            assert hasattr(position2, "_header1")
            assert hasattr(position2, "_header2")

    def test_build_request_gui_format(self, builder, header_validator_mock):
        """Test if build_request correctly calls _build_gui_format_request."""
        business_day = 20250101
        csv_file = "test.csv"
        version = True
        timestamp = 1672531200

        # Mock the header validator to return GUI format
        header_validator_mock.get_header_format.return_value = (True, False)

        # Mock the _build_gui_format_request method
        with patch.object(builder, "_build_gui_format_request") as mock_build_gui:
            mock_build_gui.return_value = "GUI_REQUEST"

            result = builder.build_request(business_day, csv_file, version, timestamp)

            mock_build_gui.assert_called_once_with(
                business_day, csv_file, version, timestamp
            )
            assert result == "GUI_REQUEST"

    def test_build_request_inner_format(self, builder, header_validator_mock):
        """Test if build_request correctly calls _build_inner_format_request."""
        business_day = 20250101
        csv_file = "test.csv"
        version = True
        timestamp = 1672531200

        # Mock the header validator to return inner format
        header_validator_mock.get_header_format.return_value = (False, True)

        # Mock the _build_inner_format_request method
        with patch.object(builder, "_build_inner_format_request") as mock_build_inner:
            mock_build_inner.return_value = "INNER_REQUEST"

            result = builder.build_request(business_day, csv_file, version, timestamp)

            mock_build_inner.assert_called_once_with(
                business_day, csv_file, version, timestamp
            )
            assert result == "INNER_REQUEST"
