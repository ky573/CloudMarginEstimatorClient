from cpme_api.api.feature.models import BaseContent


"""
Vector of volatility shifts, the unit is specified by volatility shift type. Shifted volatility is floored by 0.01 before theoretical price calculation
"""


class VolatilityShifts(BaseContent):
    """
    """
    _swagger_types = {
        'ref': 'list[VolatilityShiftsInner]',
    }

    def __init__(self):
        super(VolatilityShifts, self).__init__()
