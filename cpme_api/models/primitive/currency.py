from cpme_api.api.feature.models import BaseContent


"""
currency code
"""


class Currency(BaseContent):
    """
    """
    _primitive = 'string'

    def __init__(self):
        self.example = 'EUR'
