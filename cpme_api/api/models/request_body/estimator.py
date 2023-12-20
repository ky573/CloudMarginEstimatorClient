from cpme_api.api.feature.models import BaseContent


"""
None
"""


class BodyEstimator(BaseContent):

    _swagger_types = {
        'clearing_currency': 'ClearingCurrency',
        'is_cross_margined': 'boolean',
        'portfolio_components': 'list[BodyEstimatorPortfolioComponents]',
        'simulated_settlement_date': 'SimulatedSettlementDate',
        'snapshot': 'Snapshot',
    }

    _default_values = {
        'clearing_currency': 'EUR',
        'is_cross_margined': True,
        'portfolio_components': 'object',
        'simulated_settlement_date': 'None',
        'snapshot': 'object',
    }

    _required = ['portfolio_components']

    def __init__(self, **kwargs):
        self._clearing_currency = None
        self._is_cross_margined = None
        self._portfolio_components = None
        self._simulated_settlement_date = None
        self._snapshot = None
        super(BodyEstimator, self).__init__(**kwargs)

    @property
    def snapshot(self):
        return self._snapshot

    @snapshot.setter
    def snapshot(self, value):
        self._assign("snapshot", value)

    @property
    def clearing_currency(self):
        return self._clearing_currency

    @clearing_currency.setter
    def clearing_currency(self, value):
        self._assign("clearing_currency", value)

    @property
    def is_cross_margined(self):
        return self._is_cross_margined

    @is_cross_margined.setter
    def is_cross_margined(self, value):
        self._assign("is_cross_margined", value)

    @property
    def simulated_settlement_date(self):
        return self._simulated_settlement_date

    @simulated_settlement_date.setter
    def simulated_settlement_date(self, value):
        self._assign("simulated_settlement_date", value)

    @property
    def portfolio_components(self):
        return self._portfolio_components

    @portfolio_components.setter
    def portfolio_components(self, value):
        self._assign("portfolio_components", value)


"""
one portfolio component, only type and one structure relevant for the type is filled
"""


class BodyEstimatorPortfolioComponents(BaseContent):

    _swagger_types = {
        'cash_csv': 'CashCsv',
        'cash_json': 'CashJson',
        'etd_cp005': 'EtdCp005',
        'etd_csv': 'EtdCsv',
        'etd_portfolio': 'EtdPortfolio',
        'otc_cb202': 'OtcCb202',
        'otc_cc233': 'OtcCc233',
        'otc_csv': 'OtcCsv',
        'otc_fpml': 'OtcFpml',
        'otc_sensitivities': 'OtcSensitivities',
        'repo_json': 'RepoJson',
        'type': 'string',
        'whatif_id': 'WhatifId',
    }

    _default_values = {
        'cash_csv': 'object',
        'cash_json': 'object',
        'etd_cp005': 'object',
        'etd_csv': 'object',
        'etd_portfolio': 'object',
        'otc_cb202': 'object',
        'otc_cc233': 'object',
        'otc_csv': 'object',
        'otc_fpml': 'object',
        'otc_sensitivities': 'object',
        'repo_json': 'object',
        'type': 'etd_portfolio',
        'whatif_id': 1,
    }

    _required = ['type']

    def __init__(self, **kwargs):
        self._cash_csv = None
        self._cash_json = None
        self._etd_cp005 = None
        self._etd_csv = None
        self._etd_portfolio = None
        self._otc_cb202 = None
        self._otc_cc233 = None
        self._otc_csv = None
        self._otc_fpml = None
        self._otc_sensitivities = None
        self._repo_json = None
        self._type = None
        self._whatif_id = None
        super(BodyEstimatorPortfolioComponents, self).__init__(**kwargs)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._assign("type", value)
        if not self.type:
            self.type = "type"

    @property
    def etd_portfolio(self):
        return self._etd_portfolio

    @etd_portfolio.setter
    def etd_portfolio(self, value):
        self._assign("etd_portfolio", value)
        if not self.type:
            self.type = "etd_portfolio"

    @property
    def etd_csv(self):
        return self._etd_csv

    @etd_csv.setter
    def etd_csv(self, value):
        self._assign("etd_csv", value)
        if not self.type:
            self.type = "etd_csv"

    @property
    def etd_cp005(self):
        return self._etd_cp005

    @etd_cp005.setter
    def etd_cp005(self, value):
        self._assign("etd_cp005", value)
        if not self.type:
            self.type = "etd_cp005"

    @property
    def otc_csv(self):
        return self._otc_csv

    @otc_csv.setter
    def otc_csv(self, value):
        self._assign("otc_csv", value)
        if not self.type:
            self.type = "otc_csv"

    @property
    def otc_sensitivities(self):
        return self._otc_sensitivities

    @otc_sensitivities.setter
    def otc_sensitivities(self, value):
        self._assign("otc_sensitivities", value)
        if not self.type:
            self.type = "otc_sensitivities"

    @property
    def otc_cb202(self):
        return self._otc_cb202

    @otc_cb202.setter
    def otc_cb202(self, value):
        self._assign("otc_cb202", value)
        if not self.type:
            self.type = "otc_cb202"

    @property
    def otc_cc233(self):
        return self._otc_cc233

    @otc_cc233.setter
    def otc_cc233(self, value):
        self._assign("otc_cc233", value)
        if not self.type:
            self.type = "otc_cc233"

    @property
    def otc_fpml(self):
        return self._otc_fpml

    @otc_fpml.setter
    def otc_fpml(self, value):
        self._assign("otc_fpml", value)
        if not self.type:
            self.type = "otc_fpml"

    @property
    def cash_json(self):
        return self._cash_json

    @cash_json.setter
    def cash_json(self, value):
        self._assign("cash_json", value)
        if not self.type:
            self.type = "cash_json"

    @property
    def cash_csv(self):
        return self._cash_csv

    @cash_csv.setter
    def cash_csv(self, value):
        self._assign("cash_csv", value)
        if not self.type:
            self.type = "cash_csv"

    @property
    def repo_json(self):
        return self._repo_json

    @repo_json.setter
    def repo_json(self, value):
        self._assign("repo_json", value)
        if not self.type:
            self.type = "repo_json"

    @property
    def whatif_id(self):
        return self._whatif_id

    @whatif_id.setter
    def whatif_id(self, value):
        self._assign("whatif_id", value)
        if not self.type:
            self.type = "whatif_id"
