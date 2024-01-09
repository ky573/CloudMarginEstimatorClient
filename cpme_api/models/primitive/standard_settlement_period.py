from cpme_api.api.feature.models import BaseContent


"""
standard settlement period in days
"""


class StandardSettlementPeriod(BaseContent):
    """
    """
    _primitive = 'number'

    def __init__(self):
        self.example = 2
