from cpme_api.api.feature.models import BaseContent


"""
security ticker, upto 4 characters, can be empty
"""


class SecId(BaseContent):
    """
    """
    _primitive = 'string'

    def __init__(self):
        self.example = 'DB1'
