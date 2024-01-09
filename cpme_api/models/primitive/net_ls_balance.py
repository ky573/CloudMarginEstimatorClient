from cpme_api.api.feature.models import BaseContent


"""
Long/short balance, negative for short
"""


class NetLsBalance(BaseContent):
    """
    """
    _primitive = 'number'

    def __init__(self):
        self.example = -100
