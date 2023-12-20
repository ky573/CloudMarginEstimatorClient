from cpme_api.api.feature.models import BaseContent


"""
None
"""


class BodyConvertCashCsv(BaseContent):

    _swagger_types = {
        'csv': 'CashCsv',
    }

    _default_values = {
        'csv': 'object',
    }

    _required = ['csv']

    def __init__(self, csv=''):
        self._csv = None
        super(BodyConvertCashCsv, self).__init__(csv=csv)

    @property
    def csv(self):
        return self._csv

    @csv.setter
    def csv(self, value):
        self._assign("csv", value)
