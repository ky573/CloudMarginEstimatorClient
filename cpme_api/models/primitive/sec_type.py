from cpme_api.api.feature.models import BaseContent


"""
security type, internal categorization
"""


class SecType(BaseContent):
    """
    """
    _primitive = 'string'

    def __init__(self):
        self.example = 'SAKT'
