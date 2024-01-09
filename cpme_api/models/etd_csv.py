from cpme_api.api.feature.models import BaseContent


"""
None
"""


class EtdCsv(BaseContent):
    """
    """
    _swagger_types = {
        'csv': 'string',
    }

    _default_values = {
        'csv': """Product ID,Contract Date,Version Number,Call Put Flag,Exercise Price,Net LS Balance\nFEXD,20311219,0,,,100\nOESX,20311219,0,C,5000,-100""",
    }

    _required = ['csv']

    def __init__(self, csv=''):
        self._csv = None
        super(EtdCsv, self).__init__(csv=csv)

    @property
    def csv(self):
        return self._csv

    @csv.setter
    def csv(self, value):
        self._assign("csv", value)
