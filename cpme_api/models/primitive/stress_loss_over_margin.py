from cpme_api.api.feature.models import BaseContent


"""
stress loss over margin in given scenario (negative means loss)
"""


class StressLossOverMargin(BaseContent):
    """
    """
    _primitive = 'number'

    def __init__(self):
        self.example = -101808201.0
