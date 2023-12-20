from cpme_api.api.feature.models import BaseContent


"""
trade notional
"""


class Notional(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = 100000000
