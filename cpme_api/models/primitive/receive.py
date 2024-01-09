from cpme_api.api.feature.models import BaseContent


"""
receive leg, either Fixed rate or index plus optional spread
"""


class Receive(BaseContent):
    """
    """
    _primitive = 'string'

    def __init__(self):
        self.example = 'EUR-EURIBOR-3M +2bp'
