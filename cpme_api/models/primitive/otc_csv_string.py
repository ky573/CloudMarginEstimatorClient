from cpme_api.api.feature.models import BaseContent


"""
OTC portfolio as one string in CSV, format known from Margin Calculator GUI
"""


class OtcCsvString(BaseContent):
    """
    """
    _primitive = 'string'

    def __init__(self):
        self.example = 'internalTradeID,tradeType,currency,effectiveDate,terminationDate,legType,legSpread,legIndex,interestFixedAmount,notional,paymentPeriod,periodStartVNS,compounding,compoundingIndexPeriod,stub,firstRate,firstInterpolationTenor,secondInterpolationTenor,dayCountMethod,businessDayConvention,paymentCalendar,adjustment,rollMethod,legType,legSpread,legIndex,interestFixedAmount,notional,paymentPeriod,periodStartVNS,compounding,compoundingIndexPeriod,stub,firstRate,firstInterpolationTenor,secondInterpolationTenor,dayCountMethod,businessDayConvention,paymentCalendar,adjustment,rollMethod\n1,FRA,EUR,20/12/2018,20/08/2019,fixedLeg,0.15,,,100000000,3M,,,,,,,,ACT/360,,,,,floatingLeg,,,,100000000,3M,,,,,,,,ACT/360,,,,'
