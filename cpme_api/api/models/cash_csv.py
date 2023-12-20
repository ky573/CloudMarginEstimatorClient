from cpme_api.api.feature.models import BaseContent


"""
None
"""


class CashCsv(BaseContent):

    _swagger_types = {
        'csv': 'string',
    }

    _default_values = {
        'csv': """Security ISIN,Settlement Date,Settlement Currency,Payable Cash Amount,Traded Price,Security Quantity,CCP Trade Number,Leg Type\nDE0005810055,20220630,,,100.23,100,,""",
    }

    _required = ['csv']

    def __init__(self, csv=''):
        self._csv = None
        super(CashCsv, self).__init__(csv=csv)

    @property
    def csv(self):
        return self._csv

    @csv.setter
    def csv(self, value):
        self._assign("csv", value)
