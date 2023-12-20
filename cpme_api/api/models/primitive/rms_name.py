from cpme_api.api.feature.models import BaseContent


"""
Risk Measure Set name
"""


class RmsName(BaseContent):

    _primitive = 'string'

    def __init__(self):
        self.example = None
