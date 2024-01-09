from cpme_api.api.feature.models import BaseContent


"""
None
"""


class OtcCsv(BaseContent):
    """
    """
    _swagger_types = {
        'csv': 'OtcCsvString',
    }

    _default_values = {
        'csv': """internalTradeID,tradeType,currency,effectiveDate,terminationDate,legType,legSpread,legIndex,interestFixedAmount,notional,paymentPeriod,periodStartVNS,compounding,compoundingIndexPeriod,stub,firstRate,firstInterpolationTenor,secondInterpolationTenor,dayCountMethod,businessDayConvention,paymentCalendar,adjustment,rollMethod,legType,legSpread,legIndex,interestFixedAmount,notional,paymentPeriod,periodStartVNS,compounding,compoundingIndexPeriod,stub,firstRate,firstInterpolationTenor,secondInterpolationTenor,dayCountMethod,businessDayConvention,paymentCalendar,adjustment,rollMethod\n1,FRA,EUR,20/12/2018,20/08/2019,fixedLeg,0.15,,,100000000,3M,,,,,,,,ACT/360,,,,,floatingLeg,,,,100000000,3M,,,,,,,,ACT/360,,,,""",
    }

    _required = ['csv']

    def __init__(self, csv=''):
        self._csv = None
        super(OtcCsv, self).__init__(csv=csv)

    @property
    def csv(self):
        return self._csv

    @csv.setter
    def csv(self, value):
        self._assign("csv", value)
