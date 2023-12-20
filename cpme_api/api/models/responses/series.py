from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespSeries(BaseContent):

    _swagger_types = {
        'business_date': 'BusinessDate',
        'list_series': 'list[RespSeriesListSeries]',
        'live': 'Live',
        'live_timestamp': 'LiveTimestamp',
    }

    _default_values = {
        'business_date': '20181205',
        'list_series': 'object',
        'live': False,
        'live_timestamp': 0,
    }

    def __init__(self, **kwargs):
        self._business_date = None
        self._list_series = None
        self._live = None
        self._live_timestamp = None
        super(RespSeries, self).__init__(**kwargs)

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
    def list_series(self):
        return self._list_series

    @list_series.setter
    def list_series(self, value):
        self._assign("list_series", value)


"""
None
"""


class RespSeriesListSeries(BaseContent):

    _swagger_types = {
        'act_trade_unit_no': 'number',
        'call_put_flag': 'CallPutFlag',
        'contract_date': 'ContractDate',
        'contract_frequency': 'ContractFrequency',
        'contract_maturity': 'ContractMaturity',
        'days_to_expiration': 'number',
        'exercise_price': 'ExercisePrice',
        'exercise_style_flag': 'ExerciseStyleFlag',
        'expiry_maturity': 'ExpiryMaturity',
        'iid': 'Iid',
        'product_id': 'ProductId',
        'trade_unit_value': 'number',
        'version_number': 'VersionNumber',
    }

    _default_values = {
        'act_trade_unit_no': 'None',
        'call_put_flag': 'P',
        'contract_date': '20281215',
        'contract_frequency': 'MONTHLY',
        'contract_maturity': 202812,
        'days_to_expiration': 'None',
        'exercise_price': 2400,
        'exercise_style_flag': 'A',
        'expiry_maturity': 202812,
        'iid': 27471356,
        'product_id': 'OESX',
        'trade_unit_value': 'None',
        'version_number': '0',
    }

    _required = ['product_id', 'contract_date', 'contract_maturity', 'expiry_maturity', 'version_number', 'iid']

    def __init__(self, **kwargs):
        self._act_trade_unit_no = None
        self._call_put_flag = None
        self._contract_date = None
        self._contract_frequency = None
        self._contract_maturity = None
        self._days_to_expiration = None
        self._exercise_price = None
        self._exercise_style_flag = None
        self._expiry_maturity = None
        self._iid = None
        self._product_id = None
        self._trade_unit_value = None
        self._version_number = None
        super(RespSeriesListSeries, self).__init__(**kwargs)

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
    def contract_maturity(self):
        return self._contract_maturity

    @contract_maturity.setter
    def contract_maturity(self, value):
        self._assign("contract_maturity", value)

    @property
    def expiry_maturity(self):
        return self._expiry_maturity

    @expiry_maturity.setter
    def expiry_maturity(self, value):
        self._assign("expiry_maturity", value)

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
    def act_trade_unit_no(self):
        return self._act_trade_unit_no

    @act_trade_unit_no.setter
    def act_trade_unit_no(self, value):
        self._assign("act_trade_unit_no", value)

    @property
    def days_to_expiration(self):
        return self._days_to_expiration

    @days_to_expiration.setter
    def days_to_expiration(self, value):
        self._assign("days_to_expiration", value)

    @property
    def trade_unit_value(self):
        return self._trade_unit_value

    @trade_unit_value.setter
    def trade_unit_value(self, value):
        self._assign("trade_unit_value", value)

    @property
    def exercise_style_flag(self):
        return self._exercise_style_flag

    @exercise_style_flag.setter
    def exercise_style_flag(self, value):
        self._assign("exercise_style_flag", value)

    @property
    def contract_frequency(self):
        return self._contract_frequency

    @contract_frequency.setter
    def contract_frequency(self, value):
        self._assign("contract_frequency", value)
