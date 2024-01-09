from cpme_api.api.feature.models import BaseContent


"""
security subtype
"""


class SecuritySubtype(BaseContent):
    """
    """
    _primitive = 'string'

    _enum = ['BOND', 'EQUITY', 'SUBSCRIPTION_RIGHT']

    def __init__(self):
        self.example = 'EQUITY'
