from cpme_api.api.feature.models import BaseContent


"""
Margin figures on ETD position level. Full business key is used, it is not possible to map to input line_no one to one because positions may be aggregated or split. $primary_keys(iid,liquidation_group_split)
"""


class EtdPositionsInner(BaseContent):

    _swagger_types = {
        'call_put_flag': 'CallPutFlag',
        'component_margin': 'ComponentMargin',
        'component_margin_currency': 'ComponentMarginCurrency',
        'contract_date': 'ContractDate',
        'exercise_price': 'ExercisePrice',
        'exercise_style': 'ExerciseStyle',
        'iid': 'Iid',
        'instrument_type': 'InstrumentType',
        'line_no': 'LineNo',
        'liquidation_group': 'LiquidationGroup',
        'liquidation_group_split': 'LiquidationGroupSplit',
        'maturity': 'Maturity',
        'net_ls_balance': 'NetLsBalance',
        'premium_margin': 'number',
        'premium_margin_currency': 'string',
        'product_id': 'ProductId',
        'version_number': 'VersionNumber',
    }

    _default_values = {
        'call_put_flag': 'P',
        'component_margin': 'None',
        'component_margin_currency': 'None',
        'contract_date': '20281215',
        'exercise_price': 2400,
        'exercise_style': 'AMERICAN',
        'iid': 27471356,
        'instrument_type': 'Flex Option',
        'line_no': 1,
        'liquidation_group': 'None',
        'liquidation_group_split': 'None',
        'maturity': 202812,
        'net_ls_balance': -100,
        'premium_margin': 'None',
        'premium_margin_currency': 'None',
        'product_id': 'OESX',
        'version_number': '0',
    }

    _primary_keys = ['iid', 'liquidation_group_split']

    def __init__(self, **kwargs):
        self._call_put_flag = None
        self._component_margin = None
        self._component_margin_currency = None
        self._contract_date = None
        self._exercise_price = None
        self._exercise_style = None
        self._iid = None
        self._instrument_type = None
        self._line_no = None
        self._liquidation_group = None
        self._liquidation_group_split = None
        self._maturity = None
        self._net_ls_balance = None
        self._premium_margin = None
        self._premium_margin_currency = None
        self._product_id = None
        self._version_number = None
        super(EtdPositionsInner, self).__init__(**kwargs)

    @property
    def line_no(self):
        return self._line_no

    @line_no.setter
    def line_no(self, value):
        self._assign("line_no", value)

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, value):
        self._assign("product_id", value)

    @property
    def contract_date(self):
        return self._contract_date

    @contract_date.setter
    def contract_date(self, value):
        self._assign("contract_date", value)

    @property
    def maturity(self):
        return self._maturity

    @maturity.setter
    def maturity(self, value):
        self._assign("maturity", value)

    @property
    def call_put_flag(self):
        return self._call_put_flag

    @call_put_flag.setter
    def call_put_flag(self, value):
        self._assign("call_put_flag", value)

    @property
    def exercise_price(self):
        return self._exercise_price

    @exercise_price.setter
    def exercise_price(self, value):
        self._assign("exercise_price", value)

    @property
    def version_number(self):
        return self._version_number

    @version_number.setter
    def version_number(self, value):
        self._assign("version_number", value)

    @property
    def iid(self):
        return self._iid

    @iid.setter
    def iid(self, value):
        self._assign("iid", value)

    @property
    def instrument_type(self):
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, value):
        self._assign("instrument_type", value)

    @property
    def exercise_style(self):
        return self._exercise_style

    @exercise_style.setter
    def exercise_style(self, value):
        self._assign("exercise_style", value)

    @property
    def net_ls_balance(self):
        return self._net_ls_balance

    @net_ls_balance.setter
    def net_ls_balance(self, value):
        self._assign("net_ls_balance", value)

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
    def component_margin(self):
        return self._component_margin

    @component_margin.setter
    def component_margin(self, value):
        self._assign("component_margin", value)

    @property
    def component_margin_currency(self):
        return self._component_margin_currency

    @component_margin_currency.setter
    def component_margin_currency(self, value):
        self._assign("component_margin_currency", value)

    @property
    def premium_margin(self):
        return self._premium_margin

    @premium_margin.setter
    def premium_margin(self, value):
        self._assign("premium_margin", value)

    @property
    def premium_margin_currency(self):
        return self._premium_margin_currency

    @premium_margin_currency.setter
    def premium_margin_currency(self, value):
        self._assign("premium_margin_currency", value)
