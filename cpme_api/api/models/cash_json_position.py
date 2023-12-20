from cpme_api.api.feature.models import BaseContent


"""
$primary_keys(line_no,leg_type)
"""


class CashJsonPosition(BaseContent):

    _swagger_types = {
        'ccp_trade_mumber': 'number',
        'leg_type': 'string',
        'line_no': 'LineNo',
        'payable_cash_amount': 'number',
        'sec_isin': 'SecIsin',
        'security_quantity': 'number',
        'settlement_currency': 'string',
        'settlement_date': 'SettlementDate',
        'traded_price': 'number',
    }

    _default_values = {
        'ccp_trade_mumber': 'None',
        'leg_type': 'None',
        'line_no': 1,
        'payable_cash_amount': 1000,
        'sec_isin': 'DE0005810055',
        'security_quantity': -10,
        'settlement_currency': 'EUR',
        'settlement_date': '20210312',
        'traded_price': 100,
    }

    _primary_keys = ['line_no', 'leg_type']

    def __init__(self, **kwargs):
        self._ccp_trade_mumber = None
        self._leg_type = None
        self._line_no = None
        self._payable_cash_amount = None
        self._sec_isin = None
        self._security_quantity = None
        self._settlement_currency = None
        self._settlement_date = None
        self._traded_price = None
        super(CashJsonPosition, self).__init__(**kwargs)

    @property
    def line_no(self):
        return self._line_no

    @line_no.setter
    def line_no(self, value):
        self._assign("line_no", value)

    @property
    def sec_isin(self):
        return self._sec_isin

    @sec_isin.setter
    def sec_isin(self, value):
        self._assign("sec_isin", value)

    @property
    def settlement_date(self):
        return self._settlement_date

    @settlement_date.setter
    def settlement_date(self, value):
        self._assign("settlement_date", value)

    @property
    def settlement_currency(self):
        return self._settlement_currency

    @settlement_currency.setter
    def settlement_currency(self, value):
        self._assign("settlement_currency", value)

    @property
    def payable_cash_amount(self):
        return self._payable_cash_amount

    @payable_cash_amount.setter
    def payable_cash_amount(self, value):
        self._assign("payable_cash_amount", value)

    @property
    def traded_price(self):
        return self._traded_price

    @traded_price.setter
    def traded_price(self, value):
        self._assign("traded_price", value)

    @property
    def security_quantity(self):
        return self._security_quantity

    @security_quantity.setter
    def security_quantity(self, value):
        self._assign("security_quantity", value)

    @property
    def ccp_trade_mumber(self):
        return self._ccp_trade_mumber

    @ccp_trade_mumber.setter
    def ccp_trade_mumber(self, value):
        self._assign("ccp_trade_mumber", value)

    @property
    def leg_type(self):
        return self._leg_type

    @leg_type.setter
    def leg_type(self, value):
        self._assign("leg_type", value)
