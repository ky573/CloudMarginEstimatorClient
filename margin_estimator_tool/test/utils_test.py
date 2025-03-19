from margin_estimator_tool.src.margin_estimator_tool.core.utils import flatten_dict

class TestFlattenDict:
    def test_simple(self):
        input_dict = {"a": 1, "b": "text", "c": [1, 2, 3]}
        expected = {"a": 1, "b": "text", "c": "[1, 2, 3]"}
        assert flatten_dict(input_dict) == expected

    def test_nested(self):
        input_dict = {"a": {"b": 2, "c": "text"}}
        expected = {"a_b": 2, "a_c": "text"}
        assert flatten_dict(input_dict) == expected

    def test_deeply_nested(self):
        input_dict = {"a": {"b": {"c": 3}}}
        expected = {"a_b_c": 3}
        assert flatten_dict(input_dict) == expected

    def test_list_of_dicts(self):
        input_dict = {"a": [{"b": 1}, {"c": 2}]}
        expected = {"a_1_b": 1, "a_2_c": 2}
        assert flatten_dict(input_dict) == expected

    def test_mixed(self):
        input_dict = {"a": {"b": [1, 2, 3]}, "c": {"d": "text"}}
        expected = {"a_b": "[1, 2, 3]", "c_d": "text"}
        assert flatten_dict(input_dict) == expected

    def test_empty(self):
        assert flatten_dict({}) == {}

    def test_custom_separator(self):
        input_dict = {"a": {"b": {"c": 3}}}
        expected = {"a:b:c": 3}
        assert flatten_dict(input_dict, sep=":") == expected
