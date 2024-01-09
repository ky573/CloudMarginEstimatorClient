from cpme_api.api.feature.models import BaseContent


"""
None
"""


class GreekTypesInner(BaseContent):
    """
    """
    _primitive = 'string'

    _enum = ['DELTA', 'GAMMA', 'RHO', 'THETA', 'VEGA', 'DV01', 'EURO_DELTA', 'EURO_GAMMA', 'EURO_RHO', 'EURO_THETA', 'EURO_VEGA']

    def __init__(self):
        self.example = None
