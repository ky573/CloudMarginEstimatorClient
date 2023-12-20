from cpme_api.api.feature.models import BaseContent


"""
Volatility shift type, either relative, vola 20% shifted by 0.1 relative = 22%, or absolute, vola 20% shifted by 0.1 absolute = 20.1%
"""


class VolatilityShiftType(BaseContent):

    _primitive = 'string'

    _enum = ['RELATIVE', 'ABSOLUTE']

    def __init__(self):
        self.example = 'ABSOLUTE'
