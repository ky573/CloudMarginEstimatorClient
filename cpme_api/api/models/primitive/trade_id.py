from cpme_api.api.feature.models import BaseContent


"""
internalTradeID or tradeId as submitted in the request
"""


class TradeId(BaseContent):

    _primitive = 'string'

    def __init__(self):
        self.example = '1'
