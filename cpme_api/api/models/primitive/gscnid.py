from cpme_api.api.feature.models import BaseContent


"""
numerical id of the global scenario, used in /default_fund drilldown
"""


class Gscnid(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = 1
