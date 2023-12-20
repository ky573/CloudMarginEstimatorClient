from cpme_api.api.feature.models import BaseContent


"""
Table of DV01 sensitivities (a.k.a. deltas) of the OTC portfolio. There can be only one component of this type as input for margin calculation.
"""


class OtcSensitivities(BaseContent):

    _swagger_types = {
        'csv': 'string',
    }

    _default_values = {
        'csv': """Maturity,CHF.SARON.ON,DKK.CIBOR.6M,EUR.ESTR.ON,EUR.EURIBOR.1M,EUR.EURIBOR.1Y,EUR.EURIBOR.3M,EUR.EURIBOR.6M,GBP.SONIA.ON,JPY.TONAR.ON,NOK.NIBOR.6M,PLN.WIBOR.6M,SEK.STIBOR.3M,USD.SOFR.ON\n1M,100,,,,,,,,,,,,""",
    }

    _required = ['csv']

    def __init__(self, **kwargs):
        self._csv = None
        super(OtcSensitivities, self).__init__(**kwargs)

    @property
    def csv(self):
        return self._csv

    @csv.setter
    def csv(self, value):
        self._assign("csv", value)
