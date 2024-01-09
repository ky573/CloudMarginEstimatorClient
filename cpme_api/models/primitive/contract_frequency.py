from cpme_api.api.feature.models import BaseContent


"""
Contract frequency
"""


class ContractFrequency(BaseContent):
    """
    """
    _primitive = 'string'

    _enum = ['MONTHLY', 'WEEKLY', 'DAILY', 'FLEX', 'END_OF_MONTH']

    def __init__(self):
        self.example = 'MONTHLY'
