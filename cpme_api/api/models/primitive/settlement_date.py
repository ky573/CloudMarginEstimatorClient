from cpme_api.api.feature.models import BaseContent


"""
Settlement date as YYYYMMDD, mandatory
"""


class SettlementDate(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = 20210312
