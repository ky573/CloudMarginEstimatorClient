from cpme_api.api.feature.models import BaseContent


"""
error message applicable to the whole request
"""


class Error(BaseContent):

    _primitive = 'string'

    def __init__(self):
        self.example = 'missing portfolio_components JSON array in body JSON'
