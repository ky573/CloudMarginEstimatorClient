from cpme_api.api.feature.models import BaseContent


"""
Business date as of which the result is calculated, in YYYYMMDD format
"""


class BusinessDate(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = 20181205
