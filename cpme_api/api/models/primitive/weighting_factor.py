from cpme_api.api.feature.models import BaseContent


"""
RMS weighting factor to be applied before aggregation to LGS level
"""


class WeightingFactor(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = None
