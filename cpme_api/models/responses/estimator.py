from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespEstimator(BaseContent):
    """
    """
    _swagger_types = {
        'business_date': 'BusinessDate',
        'clearing_currency': 'ClearingCurrency',
        'drilldowns': 'EtdPositions',
        'error': 'Error',
        'errors': 'Errors',
        'live': 'Live',
        'live_timestamp': 'LiveTimestamp',
        'otc_drilldowns': 'OtcDrilldowns',
        'portfolio_margin': 'PortfolioMargin',
        'rbm_margin': 'RbmMargin',
        'what_if_portfolio_margin': 'WhatifPortfolioMargin',
    }

    _default_values = {
        'business_date': '20181205',
        'clearing_currency': 'EUR',
        'drilldowns': 'object',
        'error': 'missing portfolio_components JSON array in body JSON',
        'errors': [{'error_msg': 'Request data is invalid'}, {'line_no': 1, 'portfolio': 'ETD', 'error_msg': 'portfolio array item: missing net_ls_balance integer'}],
        'live': False,
        'live_timestamp': 0,
        'otc_drilldowns': 'object',
        'portfolio_margin': 'object',
        'rbm_margin': 'object',
        'what_if_portfolio_margin': 'object',
    }

    def __init__(self, **kwargs):
        self._business_date = None
        self._clearing_currency = None
        self._drilldowns = None
        self._error = None
        self._errors = None
        self._live = None
        self._live_timestamp = None
        self._otc_drilldowns = None
        self._portfolio_margin = None
        self._rbm_margin = None
        self._what_if_portfolio_margin = None
        super(RespEstimator, self).__init__(**kwargs)

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
    def clearing_currency(self):
        return self._clearing_currency

    @clearing_currency.setter
    def clearing_currency(self, value):
        self._assign("clearing_currency", value)

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

    @property
    def portfolio_margin(self):
        return self._portfolio_margin

    @portfolio_margin.setter
    def portfolio_margin(self, value):
        self._assign("portfolio_margin", value)

    @property
    def rbm_margin(self):
        return self._rbm_margin

    @rbm_margin.setter
    def rbm_margin(self, value):
        self._assign("rbm_margin", value)

    @property
    def what_if_portfolio_margin(self):
        return self._what_if_portfolio_margin

    @what_if_portfolio_margin.setter
    def what_if_portfolio_margin(self, value):
        self._assign("what_if_portfolio_margin", value)

    @property
    def drilldowns(self):
        return self._drilldowns

    @drilldowns.setter
    def drilldowns(self, value):
        self._assign("drilldowns", value)

    @property
    def otc_drilldowns(self):
        return self._otc_drilldowns

    @otc_drilldowns.setter
    def otc_drilldowns(self, value):
        self._assign("otc_drilldowns", value)
