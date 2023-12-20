from cpme_api.api.feature.models import BaseContent


"""
None
"""


class EtdPortfolio(BaseContent):

    _swagger_types = {
        'ref': 'list[EtdPortfolioInner]',
    }

    def __init__(self):
        super(EtdPortfolio, self).__init__()
