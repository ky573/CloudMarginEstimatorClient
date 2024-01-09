from cpme_api.api.feature.models import BaseContent


"""
None
"""


class BodyStressmatrix(BaseContent):
    """
    """
    _swagger_types = {
        'iids': 'Iids',
        'snapshot': 'Snapshot',
        'underlying_shifts_rel': 'UnderlyingShiftsRel',
        'volatility_shift_type': 'VolatilityShiftType',
        'volatility_shifts': 'VolatilityShifts',
    }

    _default_values = {
        'iids': [26807581, 27471356],
        'snapshot': 'object',
        'underlying_shifts_rel': [-0.01, 0.01],
        'volatility_shift_type': 'ABSOLUTE',
        'volatility_shifts': [-0.05, 0.05],
    }

    _required = ['iids']

    def __init__(self, **kwargs):
        self._iids = None
        self._snapshot = None
        self._underlying_shifts_rel = None
        self._volatility_shift_type = None
        self._volatility_shifts = None
        super(BodyStressmatrix, self).__init__(**kwargs)

    @property
    def snapshot(self):
        return self._snapshot

    @snapshot.setter
    def snapshot(self, value):
        self._assign("snapshot", value)

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
    def iids(self):
        return self._iids

    @iids.setter
    def iids(self, value):
        self._assign("iids", value)
