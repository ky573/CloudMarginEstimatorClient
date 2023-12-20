from cpme_api.api.feature.models import BaseContent


"""
Current liquidating margin for cash market, covering current loss
"""


class CurrentLiquidatingMargin(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = None
