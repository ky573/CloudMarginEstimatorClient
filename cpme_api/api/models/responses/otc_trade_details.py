from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespOtcTradeDetails(BaseContent):

    _swagger_types = {
        'business_date': 'BusinessDate',
        'error': 'Error',
        'errors': 'Errors',
        'live': 'Live',
        'live_timestamp': 'LiveTimestamp',
        'otc_trade_details': 'OtcTradeDetails',
    }

    _default_values = {
        'business_date': '20181205',
        'error': 'missing portfolio_components JSON array in body JSON',
        'errors': [{'error_msg': 'Request data is invalid'}, {'line_no': 1, 'portfolio': 'ETD', 'error_msg': 'portfolio array item: missing net_ls_balance integer'}],
        'live': False,
        'live_timestamp': 0,
        'otc_trade_details': 'object',
    }

    def __init__(self, **kwargs):
        self._business_date = None
        self._error = None
        self._errors = None
        self._live = None
        self._live_timestamp = None
        self._otc_trade_details = None
        super(RespOtcTradeDetails, self).__init__(**kwargs)

    @property
    def business_date(self):
        return self._business_date

    @business_date.setter
    def business_date(self, value):
        self._assign("business_date", value)

    @property
    def live(self):
        return self._live

    @live.setter
    def live(self, value):
        self._assign("live", value)

    @property
    def live_timestamp(self):
        return self._live_timestamp

    @live_timestamp.setter
    def live_timestamp(self, value):
        self._assign("live_timestamp", value)

    @property
    def otc_trade_details(self):
        return self._otc_trade_details

    @otc_trade_details.setter
    def otc_trade_details(self, value):
        self._assign("otc_trade_details", value)

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
