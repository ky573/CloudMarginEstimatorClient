from cpme_api.api.feature.models import BaseContent


"""
Margin on LGS level, higher levels can be summed on UI. Also initial margin can be calculated as a sum of all components except premium margin $primary_keys(liquidation_group,liquidation_group_split)
"""


class PortfolioMargin(BaseContent):
    """
    """
    _swagger_types = {
        'ref': 'list[PortfolioMarginInner]',
    }

    def __init__(self):
        super(PortfolioMargin, self).__init__()
