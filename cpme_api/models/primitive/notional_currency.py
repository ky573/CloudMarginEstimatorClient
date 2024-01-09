from cpme_api.api.feature.models import BaseContent


"""
notional currency
"""


class NotionalCurrency(BaseContent):
    """
    """
    _primitive = 'string'

    def __init__(self):
        self.example = 'EUR'
