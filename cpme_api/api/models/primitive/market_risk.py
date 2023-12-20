from cpme_api.api.feature.models import BaseContent


"""
Market risk from ReportCP046
"""


class MarketRisk(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = None
