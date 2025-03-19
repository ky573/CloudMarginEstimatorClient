from unittest.mock import patch, mock_open
from margin_estimator_tool.src.margin_estimator_tool.estimator.portfolio_header_validator import HeaderValidator


class TestHeaderValidator:
    def test_valid_gui_header(self):
        csv_content = "Product ID,Contract Date,Call Put Flag,Exercise Price,Version Number,Net LS Balance\n"
        with patch("builtins.open", mock_open(read_data=csv_content)):
            validator = HeaderValidator()
            assert validator.validate_headers("dummy.csv") is True
            assert validator.get_header_format() == (True, False)

    def test_valid_inner_header(self):
        csv_content = "call_put_flag,component_margin,component_margin_currency,contract_date,exercise_price,exercise_style,iid,instrument_type,line_no,liquidation_group,liquidation_group_split,maturity,net_ls_balance,premium_margin,premium_margin_currency,product_id,version_number\n"
        with patch("builtins.open", mock_open(read_data=csv_content)):
            validator = HeaderValidator()
            assert validator.validate_headers("dummy.csv") is True
            assert validator.get_header_format() == (False, True)

    def test_invalid_header(self):
        csv_content = "Invalid,Header,Data\n"
        with patch("builtins.open", mock_open(read_data=csv_content)):
            validator = HeaderValidator()
            assert validator.validate_headers("dummy.csv") is False
            assert validator.get_header_format() == (False, False)

    def test_empty_file(self):
        csv_content = ""
        with patch("builtins.open", mock_open(read_data=csv_content)):
            validator = HeaderValidator()
            assert validator.validate_headers("dummy.csv") is False
            assert validator.get_header_format() == (False, False)