from cpme_api.api.feature.models import BaseContent


"""
None
"""


class CurrencyAmount(BaseContent):
    """
    """
    _swagger_types = {
        'amount': 'number',
        'currency': 'string',
    }

    _default_values = {
        'amount': 446.37538928000043,
        'currency': 'USD',
    }

    def __init__(self, **kwargs):
        self._amount = None
        self._currency = None
        super(CurrencyAmount, self).__init__(**kwargs)

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        self._assign("currency", value)

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._assign("amount", value)
