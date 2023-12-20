from cpme_api.api.feature.models import BaseContent


"""
date as YYYYMMDD, optional and relevant only for Repos. If provided it must be greater than the snapshot date and CPME will calculate margin as if the number of calendar days between snapshot date and simulated settlement date has passed. If any Repo legs have settlement date before simulated settlement date, they will be considered as settled. Market data are taken from the snapshot date (the simulated settlement date can be in future).
"""


class SimulatedSettlementDate(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = None
