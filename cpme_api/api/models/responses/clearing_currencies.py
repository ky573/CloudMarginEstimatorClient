from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespClearingCurrencies(BaseContent):

    _swagger_types = {
        'business_date': 'BusinessDate',
        'clearing_currencies': 'list[RespClearingCurrenciesClearingCurrencies]',
        'live': 'Live',
        'live_timestamp': 'LiveTimestamp',
    }

    _default_values = {
        'business_date': '20181205',
        'clearing_currencies': 'object',
        'live': False,
        'live_timestamp': 0,
    }

    def __init__(self, **kwargs):
        self._business_date = None
        self._clearing_currencies = None
        self._live = None
        self._live_timestamp = None
        super(RespClearingCurrencies, self).__init__(**kwargs)

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
    def clearing_currencies(self):
        return self._clearing_currencies

    @clearing_currencies.setter
    def clearing_currencies(self, value):
        self._assign("clearing_currencies", value)
