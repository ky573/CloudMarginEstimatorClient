from cpme_api.api.feature.models import BaseContent


"""
estimated default fund contribution (always non-negative)
"""


class DefaultFundRequirement(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = 16634756
