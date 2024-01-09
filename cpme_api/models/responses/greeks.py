from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespGreeks(BaseContent):
    """
    """
    _swagger_types = {
        'business_date': 'BusinessDate',
        'error': 'Error',
        'errors': 'Errors',
        'greek_types': 'GreekTypes',
        'greeks': 'list[RespGreeksGreeks]',
        'live': 'Live',
        'live_timestamp': 'LiveTimestamp',
        'underlying_shifts_rel': 'UnderlyingShiftsRel',
    }

    _default_values = {
        'business_date': '20181205',
        'error': 'missing portfolio_components JSON array in body JSON',
        'errors': [{'error_msg': 'Request data is invalid'}, {'line_no': 1, 'portfolio': 'ETD', 'error_msg': 'portfolio array item: missing net_ls_balance integer'}],
        'greek_types': ['EURO_DELTA', 'EURO_VEGA'],
        'greeks': 'object',
        'live': False,
        'live_timestamp': 0,
        'underlying_shifts_rel': [-0.01, 0.01],
    }

    def __init__(self, **kwargs):
        self._business_date = None
        self._error = None
        self._errors = None
        self._greek_types = None
        self._greeks = None
        self._live = None
        self._live_timestamp = None
        self._underlying_shifts_rel = None
        super(RespGreeks, self).__init__(**kwargs)

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
    def greek_types(self):
        return self._greek_types

    @greek_types.setter
    def greek_types(self, value):
        self._assign("greek_types", value)

    @property
    def underlying_shifts_rel(self):
        return self._underlying_shifts_rel

    @underlying_shifts_rel.setter
    def underlying_shifts_rel(self, value):
        self._assign("underlying_shifts_rel", value)

    @property
    def greeks(self):
        return self._greeks

    @greeks.setter
    def greeks(self, value):
        self._assign("greeks", value)

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
Array of arrays of greeks for given instrument per greek type and per underlying shift rel, in the order given by type and shift vectors $primary_keys(iid)
"""


class RespGreeksGreeks(BaseContent):
    """
    """
    _swagger_types = {
        'iid': 'Iid',
        'values': 'list[RespGreeksValues]',
    }

    _default_values = {
        'iid': 27471356,
        'values': 'object',
    }

    _primary_keys = ['iid']

    def __init__(self, **kwargs):
        self._iid = None
        self._values = None
        super(RespGreeksGreeks, self).__init__(**kwargs)

    @property
    def iid(self):
        return self._iid

    @iid.setter
    def iid(self, value):
        self._assign("iid", value)

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._assign("values", value)
