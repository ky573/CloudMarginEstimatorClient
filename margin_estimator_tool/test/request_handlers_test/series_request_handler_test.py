from unittest.mock import patch
from margin_estimator_tool.src.margin_estimator_tool.series.series_request_handler import (
    SeriesRequestHandler,
)


class TestSeriesRequestHandler:
    """Test suite for the SeriesRequestHandler class."""

    def setup_method(self):
        """Setup test data before each test."""
        self.date = "20250318"
        self.version = "LIVE"
        self.timestamp = 1234567890
        self.to_excel = True
        self.to_json = False
        self.export_dir = "test_output_dir"
        self.products = "product1,product2"
        self.type = "option"
        self.call_put_flag = "C"
        self.filters = "exercise_price:100"
        self.template = False
        self.max_tte = 10
        self.min_tte = 1

        # Create a handler instance for testing
        self.handler = SeriesRequestHandler(
            date=self.date,
            version=self.version,
            timestamp=self.timestamp,
            to_excel=self.to_excel,
            to_json=self.to_json,
            export_dir=self.export_dir,
            products=self.products,
            type=self.type,
            call_put_flag=self.call_put_flag,
            filters=self.filters,
            template=self.template,
            max_tte=self.max_tte,
            min_tte=self.min_tte,
        )

    def test_initialization(self):
        """Test that the handler is initialized with the correct parameters."""
        assert self.handler.business_date == int(self.date)
        assert self.handler.version is True  # "LIVE" should map to True
        assert self.handler.timestamp == self.timestamp
        assert self.handler.to_excel == self.to_excel
        assert self.handler.to_json == self.to_json
        assert self.handler.export_dir == self.export_dir
        assert self.handler.products == ["product1", "product2"]
        assert self.handler.type == self.type
        assert self.handler.call_put_flag == self.call_put_flag
        assert self.handler.filters is not None  # Filters should be parsed

    def test_process_and_provide_output(self):
        """Test that data is processed and exported correctly."""
        mock_series_data = [{"product_id": "product1", "call_put_flag": "C", "days_to_expiration": 5}]

        with patch.object(self.handler, "send_request", return_value=mock_series_data), \
                patch(
                    "margin_estimator_tool.src.margin_estimator_tool.core.data_exporter.DataExporter.export") as mock_export, \
                patch.object(self.handler, "_filter_series", return_value=mock_series_data):  # Mock the filter step

            self.handler.process_and_provide_output()

            # Check that the data exporter is called with the correct arguments
            mock_export.assert_any_call(
                mock_series_data,
                "Series",
                self.export_dir,
                self.to_excel,
                self.to_json,
                str(self.date),
                True,
            )

    def test_send_request_successful(self):
        """Test sending a successful request to the series endpoint."""
        mock_response = {
            "list_series": [{"product_id": "product1", "call_put_flag": "C"}]
        }

        with patch.object(self.handler.api, "series_get", return_value=mock_response), \
                patch.object(self.handler, "_check_for_error_in_response"):
            response = self.handler.send_request()

            assert response == mock_response["list_series"]

    def test_send_request_handles_exception(self):
        """Test that an exception during the request is properly handled."""
        with patch.object(self.handler.api, "series_get", side_effect=Exception("API error")), \
                patch.object(self.handler, "_handle_request_error") as mock_handle_error:
            response = self.handler.send_request()

            assert response == []  # Empty list should be returned on error
            mock_handle_error.assert_called_once()

    def test_generate_etd_portfolio_template(self):
        """Test generating the ETD portfolio template."""
        mock_filtered_series = [
            {
                "product_id": "product1",
                "contract_date": 20250318,
                "call_put_flag": "C",
                "exercise_price": 100.0,
                "version_number": 1,
            }
        ]

        with patch(
                "margin_estimator_tool.src.margin_estimator_tool.core.data_exporter.DataExporter.export") as mock_export:
            self.handler._generate_etd_portfolio_template(mock_filtered_series)

            expected_template = [
                {
                    "Product ID": "product1",
                    "Contract Date": 20250318,
                    "Call Put Flag": "C",
                    "Exercise Price": 100.0,
                    "Version Number": 1,
                    "Net LS Balance": "",
                }
            ]
            mock_export.assert_called_once_with(
                expected_template,
                "Template",
                self.export_dir,
                self.to_excel,
                self.to_json,
                str(self.date),
                True,
            )
