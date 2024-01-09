from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespLiveSnapshots(BaseContent):
    """
    """
    _swagger_types = {
        'snapshots': 'list[RespLiveSnapshotsSnapshots]',
    }

    _default_values = {
        'snapshots': 'object',
    }

    def __init__(self, **kwargs):
        self._snapshots = None
        super(RespLiveSnapshots, self).__init__(**kwargs)

    @property
    def snapshots(self):
        return self._snapshots

    @snapshots.setter
    def snapshots(self, value):
        self._assign("snapshots", value)


"""
$primary_keys(business_date,live,live_timestamp)
"""


class RespLiveSnapshotsSnapshots(BaseContent):
    """
    """
    _swagger_types = {
        'business_date': 'BusinessDate',
        'cash_available': 'CashAvailable',
        'live': 'Live',
        'live_timestamp': 'LiveTimestamp',
        'otc_available': 'OtcAvailable',
    }

    _default_values = {
        'business_date': '20181205',
        'cash_available': 'None',
        'live': False,
        'live_timestamp': 0,
        'otc_available': True,
    }

    _primary_keys = ['business_date', 'live', 'live_timestamp']

    def __init__(self, **kwargs):
        self._business_date = None
        self._cash_available = None
        self._live = None
        self._live_timestamp = None
        self._otc_available = None
        super(RespLiveSnapshotsSnapshots, self).__init__(**kwargs)

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

    @property
    def live_timestamp(self):
        return self._live_timestamp

    @live_timestamp.setter
    def live_timestamp(self, value):
        self._assign("live_timestamp", value)
