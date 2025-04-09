"""
This module handles the building of the request body for the /estimator
endpoint for both GUI and inner format.
"""

import csv
from cpme_api.models import BodyEstimator, Snapshot
import cpme_api.models as spec
from margin_estimator_tool.estimator.portfolio_header_validator import (
    HeaderValidator,
)


class EstimatorRequestBuilder:
    """Builds request bodies for the estimator API endpoint."""

    def __init__(self, header_validator: HeaderValidator) -> None:
        """
        Initialize the EstimatorRequestBuilder instance.

        Args:
            header_validator: validator for the portfolio headers
        """
        self.header_validator = header_validator

    def build_request(
        self, business_day: int, csv_file: str, version: bool, timestamp: int
    ) -> BodyEstimator:
        """
        Builds a request body for the estimator endpoint depending on the header format.

        Args:
            business_day: The business date for the request
            csv_file: Path to the portfolio CSV file
            version: Whether to use live data
            timestamp: Timestamp for the request

        Returns:
            The built BodyEstimator object
        """
        is_gui_format, is_inner_format = self.header_validator.get_header_format()

        if is_gui_format:
            return self._build_gui_format_request(
                business_day, csv_file, version, timestamp
            )
        else:
            return self._build_inner_format_request(
                business_day, csv_file, version, timestamp
            )

    @staticmethod
    def _build_base_request(
        business_day: int, version: bool, timestamp: int
    ) -> BodyEstimator:
        """Creates the base request body with common properties."""
        request_body = BodyEstimator()
        request_body.snapshot = Snapshot()
        request_body.snapshot.live = version
        request_body.snapshot.business_date = business_day
        request_body.snapshot.live_timestamp = timestamp
        request_body.clearing_currency = "EUR"
        request_body.portfolio_components = []

        return request_body

    def _build_gui_format_request(
        self, business_day: int, csv_file: str, version: bool, timestamp: int
    ) -> BodyEstimator:
        """Builds a request for GUI format CSV files."""
        request_body = self._build_base_request(business_day, version, timestamp)

        with open(csv_file, "r", encoding="utf-8") as f:
            csv_content = f.read()

        etd_csv_comp = spec.BodyEstimatorPortfolioComponents()
        etd_csv_comp.etd_csv = spec.EtdCsv(csv=csv_content)

        request_body.portfolio_components.append(etd_csv_comp)
        return request_body

    def _build_inner_format_request(
        self, business_day: int, csv_file: str, version: bool, timestamp: int
    ) -> BodyEstimator:
        """Builds a request for inner format CSV files."""
        request_body = self._build_base_request(business_day, version, timestamp)

        etd_p_comp = spec.BodyEstimatorPortfolioComponents(type="etd_portfolio")
        etd_p_comp.etd_portfolio = []

        with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            header = next(reader)

            for row in reader:
                pc_etd = spec.EtdPositionsInner()

                for key, value in zip(header, row):
                    setattr(pc_etd, "_" + key, value)

                etd_p_comp.etd_portfolio.append(pc_etd)

        request_body.portfolio_components.append(etd_p_comp)
        return request_body
