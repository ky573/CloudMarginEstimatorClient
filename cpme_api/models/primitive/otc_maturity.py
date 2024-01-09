from cpme_api.api.feature.models import BaseContent


"""
total maturity since effective date, in years
"""


class OtcMaturity(BaseContent):
    """
    """
    _primitive = 'string'

    def __init__(self):
        self.example = '0.8Y'
