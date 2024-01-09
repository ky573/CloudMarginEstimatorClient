from cpme_api.api.feature.models import BaseContent


"""
Maturity of the instrument in YYYYMM format. Corresponds to contract year/month as shown on Eurex webpage
"""


class ContractMaturity(BaseContent):
    """
    """
    _primitive = 'number'

    def __init__(self):
        self.example = 202812
