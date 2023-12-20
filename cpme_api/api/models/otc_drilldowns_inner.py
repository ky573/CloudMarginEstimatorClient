from cpme_api.api.feature.models import BaseContent


"""
Margin figures and short trade desription on OTC trade level. Internal Trade Id is used as a key. $primary_keys(trade_id)
"""


class OtcDrilldownsInner(BaseContent):

    _swagger_types = {
        'component_margin': 'ComponentMargin',
        'component_margin_currency': 'ComponentMarginCurrency',
        'dv01': 'number',
        'ie01': 'number',
        'liquidation_group': 'LiquidationGroup',
        'liquidation_group_split': 'LiquidationGroupSplit',
        'maturity': 'OtcMaturity',
        'notional': 'Notional',
        'notional_currency': 'NotionalCurrency',
        'npv': 'number',
        'pay': 'Pay',
        'receive': 'Receive',
        'trade_id': 'TradeId',
        'type': 'OtcType',
    }

    _default_values = {
        'component_margin': 'None',
        'component_margin_currency': 'None',
        'dv01': 'None',
        'ie01': 'None',
        'liquidation_group': 'None',
        'liquidation_group_split': 'None',
        'maturity': '0.8Y',
        'notional': 100000000,
        'notional_currency': 'EUR',
        'npv': 'None',
        'pay': 'Fixed 0.15%',
        'receive': 'EUR-EURIBOR-3M +2bp',
        'trade_id': '1',
        'type': 'FRA',
    }

    _primary_keys = ['trade_id']

    def __init__(self, **kwargs):
        self._component_margin = None
        self._component_margin_currency = None
        self._dv01 = None
        self._ie01 = None
        self._liquidation_group = None
        self._liquidation_group_split = None
        self._maturity = None
        self._notional = None
        self._notional_currency = None
        self._npv = None
        self._pay = None
        self._receive = None
        self._trade_id = None
        self._type = None
        super(OtcDrilldownsInner, self).__init__(**kwargs)

    @property
    def trade_id(self):
        return self._trade_id

    @trade_id.setter
    def trade_id(self, value):
        self._assign("trade_id", value)

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
    def npv(self):
        return self._npv

    @npv.setter
    def npv(self, value):
        self._assign("npv", value)

    @property
    def dv01(self):
        return self._dv01

    @dv01.setter
    def dv01(self, value):
        self._assign("dv01", value)

    @property
    def ie01(self):
        return self._ie01

    @ie01.setter
    def ie01(self, value):
        self._assign("ie01", value)

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
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._assign("type", value)

    @property
    def pay(self):
        return self._pay

    @pay.setter
    def pay(self, value):
        self._assign("pay", value)

    @property
    def receive(self):
        return self._receive

    @receive.setter
    def receive(self, value):
        self._assign("receive", value)

    @property
    def notional(self):
        return self._notional

    @notional.setter
    def notional(self, value):
        self._assign("notional", value)

    @property
    def notional_currency(self):
        return self._notional_currency

    @notional_currency.setter
    def notional_currency(self, value):
        self._assign("notional_currency", value)

    @property
    def maturity(self):
        return self._maturity

    @maturity.setter
    def maturity(self, value):
        self._assign("maturity", value)
