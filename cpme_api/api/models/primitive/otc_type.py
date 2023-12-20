from cpme_api.api.feature.models import BaseContent


"""
FRA, FixedFloat, Basis, OIS or Inflation
"""


class OtcType(BaseContent):

    _primitive = 'string'

    def __init__(self):
        self.example = 'FRA'
