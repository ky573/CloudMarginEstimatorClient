from cpme_api.api.feature.models import BaseContent


"""
the main risk measure value for this RMS, e.g. value-at-risk for Historical or Stress simulation_type
"""


class RiskMeasureValue(BaseContent):
    """
    """
    _primitive = 'number'

    def __init__(self):
        self.example = None
