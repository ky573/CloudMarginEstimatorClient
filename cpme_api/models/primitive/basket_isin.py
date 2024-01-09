from cpme_api.api.feature.models import BaseContent


"""
is the security GC-pooling basket ISIN?
"""


class BasketIsin(BaseContent):
    """
    """
    _primitive = 'boolean'

    def __init__(self):
        self.example = False
