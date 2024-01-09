from cpme_api.api.feature.models import BaseContent


"""
Call or put flag for options. Empty for futures
"""


class CallPutFlag(BaseContent):
    """
    """
    _primitive = 'string'

    _enum = ['C', 'P', '']

    def __init__(self):
        self.example = 'P'
