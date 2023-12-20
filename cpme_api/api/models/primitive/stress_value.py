from cpme_api.api.feature.models import BaseContent


"""
stress value of the portfolio or position in given scenario (negative means loss)
"""


class StressValue(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = -107168880.0
