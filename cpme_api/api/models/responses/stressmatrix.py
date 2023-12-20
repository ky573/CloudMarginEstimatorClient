from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespStressmatrix(BaseContent):

    _swagger_types = {
        'business_date': 'BusinessDate',
        'error': 'Error',
        'errors': 'Errors',
        'live': 'Live',
        'live_timestamp': 'LiveTimestamp',
        'stress_matrix': 'list[RespStressmatrixStressMatrix]',
        'underlying_shifts_rel': 'UnderlyingShiftsRel',
        'volatility_shift_type': 'VolatilityShiftType',
        'volatility_shifts': 'VolatilityShifts',
    }

    _default_values = {
        'business_date': '20181205',
        'error': 'missing portfolio_components JSON array in body JSON',
        'errors': [{'error_msg': 'Request data is invalid'}, {'line_no': 1, 'portfolio': 'ETD', 'error_msg': 'portfolio array item: missing net_ls_balance integer'}],
        'live': False,
        'live_timestamp': 0,
        'stress_matrix': 'object',
        'underlying_shifts_rel': [-0.01, 0.01],
        'volatility_shift_type': 'ABSOLUTE',
        'volatility_shifts': [-0.05, 0.05],
    }

    def __init__(self, **kwargs):
        self._business_date = None
        self._error = None
        self._errors = None
        self._live = None
        self._live_timestamp = None
        self._stress_matrix = None
        self._underlying_shifts_rel = None
        self._volatility_shift_type = None
        self._volatility_shifts = None
        super(RespStressmatrix, self).__init__(**kwargs)

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
    def underlying_shifts_rel(self):
        return self._underlying_shifts_rel

    @underlying_shifts_rel.setter
    def underlying_shifts_rel(self, value):
        self._assign("underlying_shifts_rel", value)

    @property
    def volatility_shifts(self):
        return self._volatility_shifts

    @volatility_shifts.setter
    def volatility_shifts(self, value):
        self._assign("volatility_shifts", value)

    @property
    def volatility_shift_type(self):
        return self._volatility_shift_type

    @volatility_shift_type.setter
    def volatility_shift_type(self, value):
        self._assign("volatility_shift_type", value)

    @property
    def stress_matrix(self):
        return self._stress_matrix

    @stress_matrix.setter
    def stress_matrix(self, value):
        self._assign("stress_matrix", value)

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
Array of arrays of prices for given instrument per underlying price shift and volatility shift, in the order given by price and vola shift vectors $primary_keys(iid)
"""


class RespStressmatrixStressMatrix(BaseContent):

    _swagger_types = {
        'iid': 'Iid',
        'values': 'list[RespStressmatrixValues]',
    }

    _default_values = {
        'iid': 27471356,
        'values': 'object',
    }

    _primary_keys = ['iid']

    def __init__(self, **kwargs):
        self._iid = None
        self._values = None
        super(RespStressmatrixStressMatrix, self).__init__(**kwargs)

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
