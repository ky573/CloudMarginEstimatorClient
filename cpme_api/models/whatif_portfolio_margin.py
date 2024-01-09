from cpme_api.api.feature.models import BaseContent


"""
array of portfolio margins for what-if scenarios. Sent only if any portfolio component was marked with non-zero whatif_id in the estimator request $primary_keys(whatif_id)
"""


class WhatifPortfolioMargin(BaseContent):
    """
    """
    _swagger_types = {
        'ref': 'list[WhatifPortfolioMarginInner]',
    }

    def __init__(self):
        super(WhatifPortfolioMargin, self).__init__()
