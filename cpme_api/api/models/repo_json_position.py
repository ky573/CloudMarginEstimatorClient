from cpme_api.api.feature.models import BaseContent


"""
$primary_keys(line_no)
"""


class RepoJsonPosition(BaseContent):

    _swagger_types = {
        'buy_sell_indicator': 'string',
        'clean_price_shift': 'number',
        'currency': 'string',
        'fixed_repo_rate': 'number',
        'line_no': 'LineNo',
        'nominal': 'number',
        'sec_isin': 'SecIsin',
        'settlement_date_frontleg': 'string',
        'settlement_date_termleg': 'string',
        'trade_date': 'string',
        'trade_id': 'string',
    }

    _default_values = {
        'buy_sell_indicator': 'BUY',
        'clean_price_shift': -1,
        'currency': 'EUR',
        'fixed_repo_rate': 2.25,
        'line_no': 1,
        'nominal': 500000000,
        'sec_isin': 'DE0005810055',
        'settlement_date_frontleg': '20210316',
        'settlement_date_termleg': '20210413',
        'trade_date': '20210315',
        'trade_id': 'ABC123',
    }

    _required = ['line_no', 'sec_isin', 'trade_date', 'settlement_date_frontleg', 'settlement_date_termleg', 'buy_sell_indicator', 'nominal', 'fixed_repo_rate']

    _primary_keys = ['line_no']

    def __init__(self, **kwargs):
        self._buy_sell_indicator = None
        self._clean_price_shift = None
        self._currency = None
        self._fixed_repo_rate = None
        self._line_no = None
        self._nominal = None
        self._sec_isin = None
        self._settlement_date_frontleg = None
        self._settlement_date_termleg = None
        self._trade_date = None
        self._trade_id = None
        super(RepoJsonPosition, self).__init__(**kwargs)

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
    def trade_date(self):
        return self._trade_date

    @trade_date.setter
    def trade_date(self, value):
        self._assign("trade_date", value)

    @property
    def settlement_date_frontleg(self):
        return self._settlement_date_frontleg

    @settlement_date_frontleg.setter
    def settlement_date_frontleg(self, value):
        self._assign("settlement_date_frontleg", value)

    @property
    def settlement_date_termleg(self):
        return self._settlement_date_termleg

    @settlement_date_termleg.setter
    def settlement_date_termleg(self, value):
        self._assign("settlement_date_termleg", value)

    @property
    def buy_sell_indicator(self):
        return self._buy_sell_indicator

    @buy_sell_indicator.setter
    def buy_sell_indicator(self, value):
        self._assign("buy_sell_indicator", value)

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        self._assign("currency", value)

    @property
    def nominal(self):
        return self._nominal

    @nominal.setter
    def nominal(self, value):
        self._assign("nominal", value)

    @property
    def fixed_repo_rate(self):
        return self._fixed_repo_rate

    @fixed_repo_rate.setter
    def fixed_repo_rate(self, value):
        self._assign("fixed_repo_rate", value)

    @property
    def trade_id(self):
        return self._trade_id

    @trade_id.setter
    def trade_id(self, value):
        self._assign("trade_id", value)

    @property
    def clean_price_shift(self):
        return self._clean_price_shift

    @clean_price_shift.setter
    def clean_price_shift(self, value):
        self._assign("clean_price_shift", value)
