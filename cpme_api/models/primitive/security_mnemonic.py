from cpme_api.api.feature.models import BaseContent


"""
security mnemonic, can be empty
"""


class SecurityMnemonic(BaseContent):
    """
    """
    _primitive = 'string'

    def __init__(self):
        self.example = 'DB1'
