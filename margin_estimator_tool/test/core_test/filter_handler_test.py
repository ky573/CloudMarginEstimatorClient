"""Test suite for FilterHandler class"""

import pytest
import click
from margin_estimator_tool.src.margin_estimator_tool.core.filter_handler import FilterHandler


class TestFilterHandler:
    """Test cases for FilterHandler class"""

    def test_init(self):
        """Test initialization of FilterHandler"""
        extrafields = ["field1", "field2", "xm_eligibility"]
        numeric_values = ["field1"]

        handler = FilterHandler(extrafields, numeric_values)

        assert handler.extrafields == set(extrafields)
        assert handler.numeric_values == set(numeric_values)

        # Test with default numeric_values
        handler = FilterHandler(extrafields)
        assert handler.extrafields == set(extrafields)
        assert handler.numeric_values == set()

    def test_parse_filters_empty(self):
        """Test parsing empty or None filter string"""
        handler = FilterHandler(["field1", "field2"])

        # Test with None
        result = handler.parse_filters(None)
        assert result == {}

        # Test with empty string
        result = handler.parse_filters("")
        assert result == {}

    def test_parse_filters_valid(self):
        """Test parsing valid filter strings"""
        extrafields = ["field1", "field2", "field3", "xm_eligibility"]
        numeric_values = ["field1"]
        handler = FilterHandler(extrafields, numeric_values)

        # Test single filter
        result = handler.parse_filters("field1:123")
        assert result == {"field1": 123}

        # Test multiple filters
        result = handler.parse_filters("field1:123,field2:value,field3:another")
        assert result == {"field1": 123, "field2": "value", "field3": "another"}

        # Test boolean conversion for xm_eligibility
        result = handler.parse_filters("xm_eligibility:false")
        assert result == {"xm_eligibility": False}

        result = handler.parse_filters("xm_eligibility:true")
        assert result == {"xm_eligibility": True}

        # Test case insensitivity for boolean values
        result = handler.parse_filters("xm_eligibility:FALSE")
        assert result == {"xm_eligibility": False}

        # Test non-false value for xm_eligibility is treated as True
        result = handler.parse_filters("xm_eligibility:anything")
        assert result == {"xm_eligibility": True}

    def test_parse_filters_invalid_format(self):
        """Test parsing filter string with invalid format"""
        handler = FilterHandler(["field1", "field2"])

        # Missing value
        with pytest.raises(click.ClickException) as excinfo:
            handler.parse_filters("field1")
        assert "Invalid filter format" in str(excinfo.value)

        # Missing key
        with pytest.raises(click.ClickException) as excinfo:
            handler.parse_filters(":value")
        assert "Invalid filter key" in str(excinfo.value)

    def test_parse_filters_invalid_key(self):
        """Test parsing filter string with invalid key"""
        handler = FilterHandler(["field1", "field2"])

        with pytest.raises(click.ClickException) as excinfo:
            handler.parse_filters("invalid_field:value")
        assert "Invalid filter key" in str(excinfo.value)
        assert "Must be one of" in str(excinfo.value)

    def test_parse_filters_invalid_int_value(self):
        """Test parsing filter string with invalid integer value"""
        handler = FilterHandler(["field1", "field2"], ["field1"])

        with pytest.raises(click.ClickException) as excinfo:
            handler.parse_filters("field1:not_an_integer")
        assert "Invalid integer value" in str(excinfo.value)

    def test_filter_response_basic(self):
        """Test basic filtering of response data"""
        handler = FilterHandler(["field1", "field2"])

        data = [
            {"field1": "value1", "field2": "value2", "extra": "data1"},
            {"field1": "value1", "field2": "different", "extra": "data2"},
            {"field1": "different", "field2": "value2", "extra": "data3"},
            {"field1": "different", "field2": "different", "extra": "data4"}
        ]

        # Single filter
        filters = {"field1": "value1"}
        result = handler.filter_response(data, filters)
        assert len(result) == 2
        assert result[0]["extra"] == "data1"
        assert result[1]["extra"] == "data2"

        # Multiple filters
        filters = {"field1": "value1", "field2": "value2"}
        result = handler.filter_response(data, filters)
        assert len(result) == 1
        assert result[0]["extra"] == "data1"

        # No matching filters
        filters = {"field1": "nonexistent"}
        result = handler.filter_response(data, filters)
        assert len(result) == 0

        # Empty filters should return all data
        filters = {}
        result = handler.filter_response(data, filters)
        assert len(result) == 4

    def test_filter_response_with_int_values(self):
        """Test filtering with integer values"""
        handler = FilterHandler(["numeric_field"], ["numeric_field"])

        data = [
            {"numeric_field": 100, "name": "item1"},
            {"numeric_field": 200, "name": "item2"},
            {"numeric_field": 300, "name": "item3"}
        ]

        filters = {"numeric_field": 200}
        result = handler.filter_response(data, filters)
        assert len(result) == 1
        assert result[0]["name"] == "item2"

    def test_filter_response_with_boolean_values(self):
        """Test filtering with boolean values"""
        handler = FilterHandler(["active"])

        data = [
            {"active": True, "name": "item1"},
            {"active": False, "name": "item2"},
            {"active": True, "name": "item3"}
        ]

        filters = {"active": True}
        result = handler.filter_response(data, filters)
        assert len(result) == 2
        assert result[0]["name"] == "item1"
        assert result[1]["name"] == "item3"

    def test_filter_response_with_missing_fields(self):
        """Test filtering when items are missing filter fields"""
        handler = FilterHandler(["field1", "field2"])

        data = [
            {"field1": "value1", "field2": "value2"},
            {"field1": "value1"},  # Missing field2
            {"field2": "value2"},  # Missing field1
            {}  # Missing both
        ]

        filters = {"field1": "value1"}
        result = handler.filter_response(data, filters)
        assert len(result) == 2

        filters = {"field2": "value2"}
        result = handler.filter_response(data, filters)
        assert len(result) == 2

        filters = {"field1": "value1", "field2": "value2"}
        result = handler.filter_response(data, filters)
        assert len(result) == 1

    def test_filter_response_with_custom_filters(self):
        """Test filtering with custom filter functions"""
        handler = FilterHandler(["field1"])

        data = [
            {"field1": "value1", "field2": 5},
            {"field1": "value1", "field2": 15},
            {"field1": "value2", "field2": 25}
        ]

        # Custom filter that only accepts items where field2 > 10
        custom_filters = {
            "field2_gt_10": lambda item: item.get("field2", 0) > 10
        }

        # Apply standard filters and custom filters
        filters = {"field1": "value1"}
        result = handler.filter_response(data, filters, custom_filters)
        assert len(result) == 1
        assert result[0]["field2"] == 15

        # Apply only custom filters
        result = handler.filter_response(data, {}, custom_filters)
        assert len(result) == 2
        assert result[0]["field2"] == 15
        assert result[1]["field2"] == 25

        # Multiple custom filters
        custom_filters["field2_lt_20"] = lambda item: item.get("field2", 0) < 20
        result = handler.filter_response(data, {}, custom_filters)
        assert len(result) == 1
        assert result[0]["field2"] == 15

    def test_filter_response_with_edge_cases(self):
        """Test filter_response with edge cases"""
        handler = FilterHandler(["field1"])

        # Empty data
        result = handler.filter_response([], {"field1": "value1"})
        assert result == []

        # None in custom_filters (default parameter)
        data = [{"field1": "value1"}]
        result = handler.filter_response(data, {"field1": "value1"})
        assert len(result) == 1

        # Empty custom_filters
        result = handler.filter_response(data, {"field1": "value1"}, {})
        assert len(result) == 1