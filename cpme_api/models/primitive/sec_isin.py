from cpme_api.api.feature.models import BaseContent


"""
security ISIN, unique identifier, mandatory, upto 16 characters
"""


class SecIsin(BaseContent):
    """
    """
    _primitive = 'string'

    def __init__(self):
        self.example = 'DE0005810055'
