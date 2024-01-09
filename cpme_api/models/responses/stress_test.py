from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespStressTest(BaseContent):
    """
    """
    _swagger_types = {
        'business_date': 'BusinessDate',
        'cash_stress_test_liqu_summary': 'list[RespStressTestCashStressTestLiquSummary]',
        'cash_stress_test_liqu_value': 'list[RespStressTestCashStressTestLiquValue]',
        'errors': 'Errors',
        'live': 'Live',
        'live_timestamp': 'LiveTimestamp',
        'position_stress_test': 'list[RespStressTestPositionStressTest]',
    }

    _default_values = {
        'business_date': '20181205',
        'cash_stress_test_liqu_summary': 'object',
        'cash_stress_test_liqu_value': 'object',
        'errors': [{'error_msg': 'Request data is invalid'}, {'line_no': 1, 'portfolio': 'ETD', 'error_msg': 'portfolio array item: missing net_ls_balance integer'}],
        'live': False,
        'live_timestamp': 0,
        'position_stress_test': 'object',
    }

    def __init__(self, **kwargs):
        self._business_date = None
        self._cash_stress_test_liqu_summary = None
        self._cash_stress_test_liqu_value = None
        self._errors = None
        self._live = None
        self._live_timestamp = None
        self._position_stress_test = None
        super(RespStressTest, self).__init__(**kwargs)

    @property
    def business_date(self):
        return self._business_date

    @business_date.setter
    def business_date(self, value):
        self._assign("business_date", value)

    @property
    def live(self):
        return self._live

    @live.setter
    def live(self, value):
        self._assign("live", value)

    @property
    def live_timestamp(self):
        return self._live_timestamp

    @live_timestamp.setter
    def live_timestamp(self, value):
        self._assign("live_timestamp", value)

    @property
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, value):
        self._assign("errors", value)

    @property
    def cash_stress_test_liqu_value(self):
        return self._cash_stress_test_liqu_value

    @cash_stress_test_liqu_value.setter
    def cash_stress_test_liqu_value(self, value):
        self._assign("cash_stress_test_liqu_value", value)

    @property
    def position_stress_test(self):
        return self._position_stress_test

    @position_stress_test.setter
    def position_stress_test(self, value):
        self._assign("position_stress_test", value)

    @property
    def cash_stress_test_liqu_summary(self):
        return self._cash_stress_test_liqu_summary

    @cash_stress_test_liqu_summary.setter
    def cash_stress_test_liqu_summary(self, value):
        self._assign("cash_stress_test_liqu_summary", value)


"""
$primary_keys(line_no)
"""


class RespStressTestPositionStressTest(BaseContent):
    """
    """
    _swagger_types = {
        'call_put': 'string',
        'contract_date': 'ContractDate',
        'contract_month': 'number',
        'contract_year': 'number',
        'exercise_price': 'number',
        'expiry_day': 'number',
        'flex_contract_symbol': 'string',
        'iid': 'Iid',
        'line_no': 'LineNo',
        'liquidation_group': 'LiquidationGroup',
        'liquidation_group_split': 'LiquidationGroupSplit',
        'net_quantity_ea': 'number',
        'net_quantity_ls': 'number',
        'neutral_price': 'number',
        'product': 'ProductId',
        'stress_value': 'list[RespStressTestStressValue]',
        'version': 'string',
    }

    _default_values = {
        'call_put': '',
        'contract_date': '20281215',
        'contract_month': 1507512,
        'contract_year': 150752030,
        'exercise_price': 150750,
        'expiry_day': 150750,
        'flex_contract_symbol': '',
        'iid': 27471356,
        'line_no': 1,
        'liquidation_group': 'None',
        'liquidation_group_split': 'None',
        'net_quantity_ea': 0,
        'net_quantity_ls': 1,
        'neutral_price': 90.14623999999999,
        'product': 'OESX',
        'stress_value': 'object',
        'version': '0',
    }

    _primary_keys = ['line_no']

    def __init__(self, **kwargs):
        self._call_put = None
        self._contract_date = None
        self._contract_month = None
        self._contract_year = None
        self._exercise_price = None
        self._expiry_day = None
        self._flex_contract_symbol = None
        self._iid = None
        self._line_no = None
        self._liquidation_group = None
        self._liquidation_group_split = None
        self._net_quantity_ea = None
        self._net_quantity_ls = None
        self._neutral_price = None
        self._product = None
        self._stress_value = None
        self._version = None
        super(RespStressTestPositionStressTest, self).__init__(**kwargs)

    @property
    def line_no(self):
        return self._line_no

    @line_no.setter
    def line_no(self, value):
        self._assign("line_no", value)

    @property
    def iid(self):
        return self._iid

    @iid.setter
    def iid(self, value):
        self._assign("iid", value)

    @property
    def liquidation_group(self):
        return self._liquidation_group

    @liquidation_group.setter
    def liquidation_group(self, value):
        self._assign("liquidation_group", value)

    @property
    def liquidation_group_split(self):
        return self._liquidation_group_split

    @liquidation_group_split.setter
    def liquidation_group_split(self, value):
        self._assign("liquidation_group_split", value)

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, value):
        self._assign("product", value)

    @property
    def call_put(self):
        return self._call_put

    @call_put.setter
    def call_put(self, value):
        self._assign("call_put", value)

    @property
    def contract_date(self):
        return self._contract_date

    @contract_date.setter
    def contract_date(self, value):
        self._assign("contract_date", value)

    @property
    def contract_year(self):
        return self._contract_year

    @contract_year.setter
    def contract_year(self, value):
        self._assign("contract_year", value)

    @property
    def contract_month(self):
        return self._contract_month

    @contract_month.setter
    def contract_month(self, value):
        self._assign("contract_month", value)

    @property
    def expiry_day(self):
        return self._expiry_day

    @expiry_day.setter
    def expiry_day(self, value):
        self._assign("expiry_day", value)

    @property
    def exercise_price(self):
        return self._exercise_price

    @exercise_price.setter
    def exercise_price(self, value):
        self._assign("exercise_price", value)

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        self._assign("version", value)

    @property
    def flex_contract_symbol(self):
        return self._flex_contract_symbol

    @flex_contract_symbol.setter
    def flex_contract_symbol(self, value):
        self._assign("flex_contract_symbol", value)

    @property
    def net_quantity_ls(self):
        return self._net_quantity_ls

    @net_quantity_ls.setter
    def net_quantity_ls(self, value):
        self._assign("net_quantity_ls", value)

    @property
    def net_quantity_ea(self):
        return self._net_quantity_ea

    @net_quantity_ea.setter
    def net_quantity_ea(self, value):
        self._assign("net_quantity_ea", value)

    @property
    def neutral_price(self):
        return self._neutral_price

    @neutral_price.setter
    def neutral_price(self, value):
        self._assign("neutral_price", value)

    @property
    def stress_value(self):
        return self._stress_value

    @stress_value.setter
    def stress_value(self, value):
        self._assign("stress_value", value)


"""
$primary_keys(scnid)
"""


class RespStressTestStressValue(BaseContent):
    """
    """
    _swagger_types = {
        'scnid': 'number',
        'stress_pnl': 'CurrencyAmount',
        'stress_pnl_product_currency': 'CurrencyAmount',
        'stress_scenario_price': 'number',
        'stress_value': 'CurrencyAmount',
        'stress_value_product_currency': 'CurrencyAmount',
        'system_scn_code': 'string',
        'system_scn_purpose': 'string',
        'system_scn_text': 'string',
    }

    _default_values = {
        'scnid': 1477,
        'stress_pnl': 'object',
        'stress_pnl_product_currency': 'object',
        'stress_scenario_price': 95.296126,
        'stress_value': 'object',
        'stress_value_product_currency': 'object',
        'system_scn_code': 'HIST_PEQ01_CMM_2001',
        'system_scn_purpose': 'Clearing Fund Historical',
        'system_scn_text': 'Capital Market Move 06.12.2001',
    }

    _primary_keys = ['scnid']

    def __init__(self, **kwargs):
        self._scnid = None
        self._stress_pnl = None
        self._stress_pnl_product_currency = None
        self._stress_scenario_price = None
        self._stress_value = None
        self._stress_value_product_currency = None
        self._system_scn_code = None
        self._system_scn_purpose = None
        self._system_scn_text = None
        super(RespStressTestStressValue, self).__init__(**kwargs)

    @property
    def scnid(self):
        return self._scnid

    @scnid.setter
    def scnid(self, value):
        self._assign("scnid", value)

    @property
    def stress_value(self):
        return self._stress_value

    @stress_value.setter
    def stress_value(self, value):
        self._assign("stress_value", value)

    @property
    def stress_pnl(self):
        return self._stress_pnl

    @stress_pnl.setter
    def stress_pnl(self, value):
        self._assign("stress_pnl", value)

    @property
    def stress_value_product_currency(self):
        return self._stress_value_product_currency

    @stress_value_product_currency.setter
    def stress_value_product_currency(self, value):
        self._assign("stress_value_product_currency", value)

    @property
    def stress_pnl_product_currency(self):
        return self._stress_pnl_product_currency

    @stress_pnl_product_currency.setter
    def stress_pnl_product_currency(self, value):
        self._assign("stress_pnl_product_currency", value)

    @property
    def stress_scenario_price(self):
        return self._stress_scenario_price

    @stress_scenario_price.setter
    def stress_scenario_price(self, value):
        self._assign("stress_scenario_price", value)

    @property
    def system_scn_code(self):
        return self._system_scn_code

    @system_scn_code.setter
    def system_scn_code(self, value):
        self._assign("system_scn_code", value)

    @property
    def system_scn_text(self):
        return self._system_scn_text

    @system_scn_text.setter
    def system_scn_text(self, value):
        self._assign("system_scn_text", value)

    @property
    def system_scn_purpose(self):
        return self._system_scn_purpose

    @system_scn_purpose.setter
    def system_scn_purpose(self, value):
        self._assign("system_scn_purpose", value)
