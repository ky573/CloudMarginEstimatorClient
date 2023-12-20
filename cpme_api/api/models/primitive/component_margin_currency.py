from cpme_api.api.feature.models import BaseContent


"""
Currency of component margin
"""


class ComponentMarginCurrency(BaseContent):

    _primitive = 'string'

    def __init__(self):
        self.example = None
