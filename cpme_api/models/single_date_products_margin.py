from cpme_api.api.feature.models import BaseContent


"""
indicative margin for one date
"""


class SingleDateProductsMargin(BaseContent):
    """
    """
    _swagger_types = {
        'business_date': 'BusinessDate',
        'list_margins': 'list[ProductMarginLongShort]',
        'live': 'Live',
        'live_timestamp': 'LiveTimestamp',
    }

    _default_values = {
        'business_date': '20181205',
        'list_margins': 'object',
        'live': False,
        'live_timestamp': 0,
    }

    def __init__(self, **kwargs):
        self._business_date = None
        self._list_margins = None
        self._live = None
        self._live_timestamp = None
        super(SingleDateProductsMargin, self).__init__(**kwargs)

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
    def list_margins(self):
        return self._list_margins

    @list_margins.setter
    def list_margins(self, value):
        self._assign("list_margins", value)
