from cpme_api.api.feature.models import BaseContent


"""
stress value of the portfolio in given scenario (negative means loss), the market risk part (liquidity risk not included)
"""


class StressValueMarketRisk(BaseContent):
    """
    """
    _primitive = 'number'

    def __init__(self):
        self.example = -107168880.0
