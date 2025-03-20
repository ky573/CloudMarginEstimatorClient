import pytest
from margin_estimator_tool.src.margin_estimator_tool.estimator.margin_calculator.extractor import Extractor


class TestExtractor:
    """Test suite for the Extractor class."""

    def test_initial_state(self):
        """Tests that the extractor starts with empty lists."""
        extractor = Extractor()
        assert extractor.initial_margins == []
        assert extractor.dates == []

    def test_extract_data_single_entry(self):
        """Tests extraction of a single data entry."""
        extractor = Extractor()
        sample_data = {
            "business_date": "20240318",
            "portfolio_margin": [{"initial_margin": "1500.75"}],
        }

        extractor.extract_data(sample_data)

        assert extractor.dates == [20240318]
        assert extractor.initial_margins == [1500.75]

    def test_extract_data_multiple_entries(self):
        """Tests extraction of multiple data entries."""
        extractor = Extractor()
        sample_data_1 = {
            "business_date": "20240318",
            "portfolio_margin": [{"initial_margin": "1500.75"}],
        }
        sample_data_2 = {
            "business_date": "20240319",
            "portfolio_margin": [{"initial_margin": "1600.50"}],
        }

        extractor.extract_data(sample_data_1)
        extractor.extract_data(sample_data_2)

        assert extractor.dates == [20240318, 20240319]
        assert extractor.initial_margins == [1500.75, 1600.50]

    def test_extract_data_invalid_data(self):
        """Tests handling of invalid data formats."""
        extractor = Extractor()
        invalid_data = {"business_date": "20240318"}  # Missing "portfolio_margin"

        with pytest.raises(KeyError):
            extractor.extract_data(invalid_data)

        invalid_data_2 = {
            "business_date": "20240318",
            "portfolio_margin": [{}],  # Missing "initial_margin"
        }

        with pytest.raises(KeyError):
            extractor.extract_data(invalid_data_2)
