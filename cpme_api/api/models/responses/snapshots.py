from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespSnapshots(BaseContent):

    _swagger_types = {
        'snapshots': 'list[RespSnapshotsSnapshots]',
    }

    _default_values = {
        'snapshots': 'object',
    }

    def __init__(self, **kwargs):
        self._snapshots = None
        super(RespSnapshots, self).__init__(**kwargs)

    @property
    def snapshots(self):
        return self._snapshots

    @snapshots.setter
    def snapshots(self, value):
        self._assign("snapshots", value)


"""
$primary_keys(business_date,live)
"""


class RespSnapshotsSnapshots(BaseContent):

    _swagger_types = {
        'business_date': 'BusinessDate',
        'cash_available': 'CashAvailable',
        'live': 'Live',
        'otc_available': 'OtcAvailable',
    }

    _default_values = {
        'business_date': '20181205',
        'cash_available': 'None',
        'live': False,
        'otc_available': True,
    }

    _primary_keys = ['business_date', 'live']

    def __init__(self, **kwargs):
        self._business_date = None
        self._cash_available = None
        self._live = None
        self._otc_available = None
        super(RespSnapshotsSnapshots, self).__init__(**kwargs)

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
    def otc_available(self):
        return self._otc_available

    @otc_available.setter
    def otc_available(self, value):
        self._assign("otc_available", value)

    @property
    def cash_available(self):
        return self._cash_available

    @cash_available.setter
    def cash_available(self, value):
        self._assign("cash_available", value)
