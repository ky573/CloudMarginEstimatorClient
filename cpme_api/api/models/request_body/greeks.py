from cpme_api.api.feature.models import BaseContent


"""
None
"""


class BodyGreeks(BaseContent):

    _swagger_types = {
        'greek_types': 'GreekTypes',
        'iids': 'Iids',
        'snapshot': 'Snapshot',
        'underlying_shifts_rel': 'UnderlyingShiftsRel',
    }

    _default_values = {
        'greek_types': ['EURO_DELTA', 'EURO_VEGA'],
        'iids': [26807581, 27471356],
        'snapshot': 'object',
        'underlying_shifts_rel': [-0.01, 0.01],
    }

    _required = ['greek_types', 'iids']

    def __init__(self, **kwargs):
        self._greek_types = None
        self._iids = None
        self._snapshot = None
        self._underlying_shifts_rel = None
        super(BodyGreeks, self).__init__(**kwargs)

    @property
    def snapshot(self):
        return self._snapshot

    @snapshot.setter
    def snapshot(self, value):
        self._assign("snapshot", value)

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
    def iids(self):
        return self._iids

    @iids.setter
    def iids(self, value):
        self._assign("iids", value)
