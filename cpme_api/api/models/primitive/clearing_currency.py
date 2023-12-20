from cpme_api.api.feature.models import BaseContent


"""
currency code of the currency in which the result should be calculated
"""


class ClearingCurrency(BaseContent):

    _primitive = 'string'

    def __init__(self):
        self.example = 'EUR'
