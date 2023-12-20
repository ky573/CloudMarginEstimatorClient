from cpme_api.api.feature.models import BaseContent


"""
None
"""


class BodyOtcTradeDetails(BaseContent):

    _swagger_types = {
        'portfolio_components': 'list[BodyOtcTradeDetailsPortfolioComponents]',
        'snapshot': 'Snapshot',
    }

    _default_values = {
        'portfolio_components': 'object',
        'snapshot': 'object',
    }

    _required = ['portfolio_components']

    def __init__(self, **kwargs):
        self._portfolio_components = None
        self._snapshot = None
        super(BodyOtcTradeDetails, self).__init__(**kwargs)

    @property
    def snapshot(self):
        return self._snapshot

    @snapshot.setter
    def snapshot(self, value):
        self._assign("snapshot", value)

    @property
    def portfolio_components(self):
        return self._portfolio_components

    @portfolio_components.setter
    def portfolio_components(self, value):
        self._assign("portfolio_components", value)


"""
one portfolio component, only type and one structure relevant for the type is filled
"""


class BodyOtcTradeDetailsPortfolioComponents(BaseContent):

    _swagger_types = {
        'otc_cb202': 'OtcCb202',
        'otc_csv': 'OtcCsv',
        'otc_fpml': 'OtcFpml',
        'type': 'string',
    }

    _default_values = {
        'otc_cb202': 'object',
        'otc_csv': 'object',
        'otc_fpml': 'object',
        'type': 'etd_portfolio',
    }

    _required = ['type']

    def __init__(self, **kwargs):
        self._otc_cb202 = None
        self._otc_csv = None
        self._otc_fpml = None
        self._type = None
        super(BodyOtcTradeDetailsPortfolioComponents, self).__init__(**kwargs)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._assign("type", value)
        if not self.type:
            self.type = "type"

    @property
    def otc_csv(self):
        return self._otc_csv

    @otc_csv.setter
    def otc_csv(self, value):
        self._assign("otc_csv", value)
        if not self.type:
            self.type = "otc_csv"

    @property
    def otc_cb202(self):
        return self._otc_cb202

    @otc_cb202.setter
    def otc_cb202(self, value):
        self._assign("otc_cb202", value)
        if not self.type:
            self.type = "otc_cb202"

    @property
    def otc_fpml(self):
        return self._otc_fpml

    @otc_fpml.setter
    def otc_fpml(self, value):
        self._assign("otc_fpml", value)
        if not self.type:
            self.type = "otc_fpml"
