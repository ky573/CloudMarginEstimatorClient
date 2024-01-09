from cpme_api.api.feature.models import BaseContent


"""
Risk Measure Set type
"""


class SimulationType(BaseContent):
    """
    """
    _primitive = 'string'

    _enum = ['Historical', 'Stress', 'Event']

    def __init__(self):
        self.example = None
