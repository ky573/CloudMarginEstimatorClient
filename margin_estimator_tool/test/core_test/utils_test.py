"""Test suite for the flatten_dict utility function."""

from margin_estimator_tool.core.utils import flatten_dict


class TestFlattenDict:
    """Tests for the flatten_dict function which converts nested dictionaries to flat dictionaries."""

    def test_simple(self):
        """Test flattening a dictionary with simple key-value pairs and a list."""
        input_dict = {"a": 1, "b": "text", "c": [1, 2, 3]}
        expected = {"a": 1, "b": "text", "c": "[1, 2, 3]"}
        assert flatten_dict(input_dict) == expected

    def test_nested(self):
        """Test flattening a dictionary with one level of nesting."""
        input_dict = {"a": {"b": 2, "c": "text"}}
        expected = {"a_b": 2, "a_c": "text"}
        assert flatten_dict(input_dict) == expected

    def test_deeply_nested(self):
        """Test flattening a dictionary with multiple levels of nesting."""
        input_dict = {"a": {"b": {"c": 3}}}
        expected = {"a_b_c": 3}
        assert flatten_dict(input_dict) == expected

    def test_list_of_dicts(self):
        """Test flattening a dictionary containing a list of dictionaries."""
        input_dict = {"a": [{"b": 1}, {"c": 2}]}
        expected = {"a_1_b": 1, "a_2_c": 2}
        assert flatten_dict(input_dict) == expected

    def test_mixed(self):
        """Test flattening a dictionary with mixed nesting types."""
        input_dict = {"a": {"b": [1, 2, 3]}, "c": {"d": "text"}}
        expected = {"a_b": "[1, 2, 3]", "c_d": "text"}
        assert flatten_dict(input_dict) == expected

    def test_empty(self):
        """Test flattening an empty dictionary."""
        assert flatten_dict({}) == {}

    def test_custom_separator(self):
        """Test flattening a dictionary with a custom separator."""
        input_dict = {"a": {"b": {"c": 3}}}
        expected = {"a:b:c": 3}
        assert flatten_dict(input_dict, sep=":") == expected
