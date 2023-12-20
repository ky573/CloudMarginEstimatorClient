from cpme_api.api.feature.models import BaseContent


"""
details of one OTC trade $primary_keys(trade_id)
"""


class OtcTradeDetailsInner(BaseContent):

    _swagger_types = {
        'maturity': 'OtcMaturity',
        'notional': 'Notional',
        'notional_currency': 'NotionalCurrency',
        'pay': 'Pay',
        'receive': 'Receive',
        'trade_id': 'TradeId',
        'type': 'OtcType',
    }

    _default_values = {
        'maturity': '0.8Y',
        'notional': 100000000,
        'notional_currency': 'EUR',
        'pay': 'Fixed 0.15%',
        'receive': 'EUR-EURIBOR-3M +2bp',
        'trade_id': '1',
        'type': 'FRA',
    }

    _primary_keys = ['trade_id']

    def __init__(self, **kwargs):
        self._maturity = None
        self._notional = None
        self._notional_currency = None
        self._pay = None
        self._receive = None
        self._trade_id = None
        self._type = None
        super(OtcTradeDetailsInner, self).__init__(**kwargs)

    @property
    def trade_id(self):
        return self._trade_id

    @trade_id.setter
    def trade_id(self, value):
        self._assign("trade_id", value)

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
