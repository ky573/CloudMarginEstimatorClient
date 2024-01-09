from cpme_api.api.feature.models import BaseContent


"""
name of the global stress scenario
"""


class GlobalScenario(BaseContent):
    """
    """
    _primitive = 'string'

    def __init__(self):
        self.example = 'Lehman crash 15.09.2008'
