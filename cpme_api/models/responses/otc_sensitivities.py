from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespOtcSensitivities(BaseContent):
    """
    """
    _swagger_types = {
        'business_date': 'BusinessDate',
        'csv': 'string',
        'curves': 'list[RespOtcSensitivitiesCurves]',
        'dv01_per_maturity': 'list[RespOtcSensitivitiesDv01PerMaturity]',
        'error': 'Error',
        'errors': 'Errors',
        'live': 'Live',
        'live_timestamp': 'LiveTimestamp',
    }

    _default_values = {
        'business_date': '20181205',
        'csv': """None""",
        'curves': 'object',
        'dv01_per_maturity': 'object',
        'error': 'missing portfolio_components JSON array in body JSON',
        'errors': [{'error_msg': 'Request data is invalid'}, {'line_no': 1, 'portfolio': 'ETD', 'error_msg': 'portfolio array item: missing net_ls_balance integer'}],
        'live': False,
        'live_timestamp': 0,
    }

    def __init__(self, **kwargs):
        self._business_date = None
        self._csv = None
        self._curves = None
        self._dv01_per_maturity = None
        self._error = None
        self._errors = None
        self._live = None
        self._live_timestamp = None
        super(RespOtcSensitivities, self).__init__(**kwargs)

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
    def curves(self):
        return self._curves

    @curves.setter
    def curves(self, value):
        self._assign("curves", value)

    @property
    def dv01_per_maturity(self):
        return self._dv01_per_maturity

    @dv01_per_maturity.setter
    def dv01_per_maturity(self, value):
        self._assign("dv01_per_maturity", value)

    @property
    def csv(self):
        return self._csv

    @csv.setter
    def csv(self, value):
        self._assign("csv", value)

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._assign("error", value)

    @property
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, value):
        self._assign("errors", value)


"""
DV01 for different curves of one maturity $primary_keys(maturity)
"""


class RespOtcSensitivitiesDv01PerMaturity(BaseContent):
    """
    """
    _swagger_types = {
        'dv01': 'list[RespOtcSensitivitiesDv01]',
        'maturity': 'OtcMaturity',
    }

    _default_values = {
        'dv01': 'object',
        'maturity': '0.8Y',
    }

    _primary_keys = ['maturity']

    def __init__(self, **kwargs):
        self._dv01 = None
        self._maturity = None
        super(RespOtcSensitivitiesDv01PerMaturity, self).__init__(**kwargs)

    @property
    def maturity(self):
        return self._maturity

    @maturity.setter
    def maturity(self, value):
        self._assign("maturity", value)

    @property
    def dv01(self):
        return self._dv01

    @dv01.setter
    def dv01(self, value):
        self._assign("dv01", value)
