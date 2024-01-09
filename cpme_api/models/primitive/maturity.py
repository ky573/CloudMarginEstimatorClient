from cpme_api.api.feature.models import BaseContent


"""
Maturity of the instrument in YYYYMM or YYYYMMDD format. Day mandatory for flex. Corresponds to contract year/month as shown on Eurex webpage
"""


class Maturity(BaseContent):
    """
    """
    _primitive = 'number'

    def __init__(self):
        self.example = 202812
