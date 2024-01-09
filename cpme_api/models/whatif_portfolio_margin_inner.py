from cpme_api.api.feature.models import BaseContent


"""
array of portfolio margins for what-if scenarios. Sent only if any portfolio component was marked with non-zero whatif_id in the estimator request $primary_keys(whatif_id)
"""


class WhatifPortfolioMarginInner(BaseContent):
    """
    """
    _swagger_types = {
        'portfolio_margin': 'PortfolioMargin',
        'whatif_id': 'WhatifId',
    }

    _default_values = {
        'portfolio_margin': 'object',
        'whatif_id': 1,
    }

    _primary_keys = ['whatif_id']

    def __init__(self, **kwargs):
        self._portfolio_margin = None
        self._whatif_id = None
        super(WhatifPortfolioMarginInner, self).__init__(**kwargs)

    @property
    def whatif_id(self):
        return self._whatif_id

    @whatif_id.setter
    def whatif_id(self, value):
        self._assign("whatif_id", value)

    @property
    def portfolio_margin(self):
        return self._portfolio_margin

    @portfolio_margin.setter
    def portfolio_margin(self, value):
        self._assign("portfolio_margin", value)
