from cpme_api.api.feature.models import BaseContent


"""
Optional point in time as of which the result is calculated. If only business_date is specified, latest snapshot from that business date is used. If only live=False is specified, last EOD is used. The timestamp is used only when live is true.
"""


class Snapshot(BaseContent):
    """
    """
    _swagger_types = {
        'business_date': 'BusinessDate',
        'live': 'Live',
        'live_timestamp': 'LiveTimestamp',
    }

    _default_values = {
        'business_date': '20181205',
        'live': False,
        'live_timestamp': 0,
    }

    def __init__(self, **kwargs):
        self._business_date = None
        self._live = None
        self._live_timestamp = None
        super(Snapshot, self).__init__(**kwargs)

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
