from cpme_api.api.feature.models import BaseContent


"""
Version number. Valid for both options and futures
"""


class VersionNumber(BaseContent):

    _primitive = 'string'

    def __init__(self):
        self.example = '0'
