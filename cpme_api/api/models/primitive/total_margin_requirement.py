from cpme_api.api.feature.models import BaseContent


"""
additional liquidity risk in given scenario
"""


class TotalMarginRequirement(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = 5362113.0
