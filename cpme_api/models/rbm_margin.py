from cpme_api.api.feature.models import BaseContent


"""
RBM margin for cash market:
- for each margin class: AM and CLM in margin class currency, corresponding to CI050 report
  - for each ISIN/settlement date combination from the margin class: current liquidating margin, net cash position and net security position, corresponding to CC711 report (if there are multiple records for ISIN/settlement date in CC711, the values are summed)
"""


class RbmMargin(BaseContent):
    """
    """
    _swagger_types = {
        'margin_classes': 'list[RbmMarginMarginClasses]',
    }

    _default_values = {
        'margin_classes': 'object',
    }

    def __init__(self, **kwargs):
        self._margin_classes = None
        super(RbmMargin, self).__init__(**kwargs)

    @property
    def margin_classes(self):
        return self._margin_classes

    @margin_classes.setter
    def margin_classes(self, value):
        self._assign("margin_classes", value)


"""
Margin on margin class level $primary_keys(margin_class_code)
"""


class RbmMarginMarginClasses(BaseContent):
    """
    """
    _swagger_types = {
        'additional_margin': 'AdditionalMargin',
        'additional_margin_before_grouping': 'AdditionalMarginBeforeGrouping',
        'cash_interest_rate': 'number',
        'current_liquidating_margin': 'CurrentLiquidatingMargin',
        'margin_class_code': 'MarginClassCode',
        'margin_class_currency': 'string',
        'margin_group_code': 'MarginGroupCode',
        'margin_parameter': 'number',
        'margin_parameter_flag': 'string',
        'positions': 'list[RbmMarginPositions]',
    }

    _default_values = {
        'additional_margin': 'None',
        'additional_margin_before_grouping': 'None',
        'cash_interest_rate': -0.566,
        'current_liquidating_margin': 'None',
        'margin_class_code': 'DB10',
        'margin_class_currency': 'USD',
        'margin_group_code': 'None',
        'margin_parameter': 3.5,
        'margin_parameter_flag': 'P',
        'positions': 'object',
    }

    _primary_keys = ['margin_class_code']

    def __init__(self, **kwargs):
        self._additional_margin = None
        self._additional_margin_before_grouping = None
        self._cash_interest_rate = None
        self._current_liquidating_margin = None
        self._margin_class_code = None
        self._margin_class_currency = None
        self._margin_group_code = None
        self._margin_parameter = None
        self._margin_parameter_flag = None
        self._positions = None
        super(RbmMarginMarginClasses, self).__init__(**kwargs)

    @property
    def margin_class_code(self):
        return self._margin_class_code

    @margin_class_code.setter
    def margin_class_code(self, value):
        self._assign("margin_class_code", value)

    @property
    def margin_group_code(self):
        return self._margin_group_code

    @margin_group_code.setter
    def margin_group_code(self, value):
        self._assign("margin_group_code", value)

    @property
    def margin_parameter(self):
        return self._margin_parameter

    @margin_parameter.setter
    def margin_parameter(self, value):
        self._assign("margin_parameter", value)

    @property
    def margin_parameter_flag(self):
        return self._margin_parameter_flag

    @margin_parameter_flag.setter
    def margin_parameter_flag(self, value):
        self._assign("margin_parameter_flag", value)

    @property
    def cash_interest_rate(self):
        return self._cash_interest_rate

    @cash_interest_rate.setter
    def cash_interest_rate(self, value):
        self._assign("cash_interest_rate", value)

    @property
    def additional_margin(self):
        return self._additional_margin

    @additional_margin.setter
    def additional_margin(self, value):
        self._assign("additional_margin", value)

    @property
    def additional_margin_before_grouping(self):
        return self._additional_margin_before_grouping

    @additional_margin_before_grouping.setter
    def additional_margin_before_grouping(self, value):
        self._assign("additional_margin_before_grouping", value)

    @property
    def current_liquidating_margin(self):
        return self._current_liquidating_margin

    @current_liquidating_margin.setter
    def current_liquidating_margin(self, value):
        self._assign("current_liquidating_margin", value)

    @property
    def margin_class_currency(self):
        return self._margin_class_currency

    @margin_class_currency.setter
    def margin_class_currency(self, value):
        self._assign("margin_class_currency", value)

    @property
    def positions(self):
        return self._positions

    @positions.setter
    def positions(self, value):
        self._assign("positions", value)


"""
Positions of the margin class $primary_keys(line_no)
"""


class RbmMarginPositions(BaseContent):
    """
    """
    _swagger_types = {
        'amount_clv_cash': 'number',
        'amount_clv_secu': 'number',
        'current_liquidating_margin': 'CurrentLiquidatingMargin',
        'line_no': 'LineNo',
        'net_cash_position': 'number',
        'net_security_position': 'number',
        'sec_isin': 'SecIsin',
        'sec_name': 'SecName',
        'settlement_date': 'SettlementDate',
        'trade_id': 'TradeId',
    }

    _default_values = {
        'amount_clv_cash': 'None',
        'amount_clv_secu': 'None',
        'current_liquidating_margin': 'None',
        'line_no': 1,
        'net_cash_position': 'None',
        'net_security_position': 'None',
        'sec_isin': 'DE0005810055',
        'sec_name': 'DEUTSCHE BOERSE AG',
        'settlement_date': '20210312',
        'trade_id': '1',
    }

    _primary_keys = ['line_no']

    def __init__(self, **kwargs):
        self._amount_clv_cash = None
        self._amount_clv_secu = None
        self._current_liquidating_margin = None
        self._line_no = None
        self._net_cash_position = None
        self._net_security_position = None
        self._sec_isin = None
        self._sec_name = None
        self._settlement_date = None
        self._trade_id = None
        super(RbmMarginPositions, self).__init__(**kwargs)

    @property
    def line_no(self):
        return self._line_no

    @line_no.setter
    def line_no(self, value):
        self._assign("line_no", value)

    @property
    def sec_isin(self):
        return self._sec_isin

    @sec_isin.setter
    def sec_isin(self, value):
        self._assign("sec_isin", value)

    @property
    def sec_name(self):
        return self._sec_name

    @sec_name.setter
    def sec_name(self, value):
        self._assign("sec_name", value)

    @property
    def settlement_date(self):
        return self._settlement_date

    @settlement_date.setter
    def settlement_date(self, value):
        self._assign("settlement_date", value)

    @property
    def net_security_position(self):
        return self._net_security_position

    @net_security_position.setter
    def net_security_position(self, value):
        self._assign("net_security_position", value)

    @property
    def net_cash_position(self):
        return self._net_cash_position

    @net_cash_position.setter
    def net_cash_position(self, value):
        self._assign("net_cash_position", value)

    @property
    def amount_clv_secu(self):
        return self._amount_clv_secu

    @amount_clv_secu.setter
    def amount_clv_secu(self, value):
        self._assign("amount_clv_secu", value)

    @property
    def amount_clv_cash(self):
        return self._amount_clv_cash

    @amount_clv_cash.setter
    def amount_clv_cash(self, value):
        self._assign("amount_clv_cash", value)

    @property
    def current_liquidating_margin(self):
        return self._current_liquidating_margin

    @current_liquidating_margin.setter
    def current_liquidating_margin(self, value):
        self._assign("current_liquidating_margin", value)

    @property
    def trade_id(self):
        return self._trade_id

    @trade_id.setter
    def trade_id(self, value):
        self._assign("trade_id", value)
