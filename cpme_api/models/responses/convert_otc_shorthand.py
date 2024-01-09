from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespConvertOtcShorthand(BaseContent):
    """
    """
    _swagger_types = {
        'error': 'Error',
        'errors': 'Errors',
        'otc_csv': 'OtcCsvString',
        'otc_trade_details': 'OtcTradeDetails',
    }

    _default_values = {
        'error': 'missing portfolio_components JSON array in body JSON',
        'errors': [{'error_msg': 'Request data is invalid'}, {'line_no': 1, 'portfolio': 'ETD', 'error_msg': 'portfolio array item: missing net_ls_balance integer'}],
        'otc_csv': """internalTradeID,tradeType,currency,effectiveDate,terminationDate,legType,legSpread,legIndex,interestFixedAmount,notional,paymentPeriod,periodStartVNS,compounding,compoundingIndexPeriod,stub,firstRate,firstInterpolationTenor,secondInterpolationTenor,dayCountMethod,businessDayConvention,paymentCalendar,adjustment,rollMethod,legType,legSpread,legIndex,interestFixedAmount,notional,paymentPeriod,periodStartVNS,compounding,compoundingIndexPeriod,stub,firstRate,firstInterpolationTenor,secondInterpolationTenor,dayCountMethod,businessDayConvention,paymentCalendar,adjustment,rollMethod\n1,FRA,EUR,20/12/2018,20/08/2019,fixedLeg,0.15,,,100000000,3M,,,,,,,,ACT/360,,,,,floatingLeg,,,,100000000,3M,,,,,,,,ACT/360,,,,""",
        'otc_trade_details': 'object',
    }

    def __init__(self, **kwargs):
        self._error = None
        self._errors = None
        self._otc_csv = None
        self._otc_trade_details = None
        super(RespConvertOtcShorthand, self).__init__(**kwargs)

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._assign("error", value)

    @property
    def errors(self):
        return self._errors

    @errors.setter
    def errors(self, value):
        self._assign("errors", value)

    @property
    def otc_csv(self):
        return self._otc_csv

    @otc_csv.setter
    def otc_csv(self, value):
        self._assign("otc_csv", value)

    @property
    def otc_trade_details(self):
        return self._otc_trade_details

    @otc_trade_details.setter
    def otc_trade_details(self, value):
        self._assign("otc_trade_details", value)
