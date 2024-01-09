from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespSecurities(BaseContent):
    """
    """
    _swagger_types = {
        'business_date': 'BusinessDate',
        'live': 'Live',
        'live_timestamp': 'LiveTimestamp',
        'securities': 'list[RespSecuritiesSecurities]',
    }

    _default_values = {
        'business_date': '20181205',
        'live': False,
        'live_timestamp': 0,
        'securities': 'object',
    }

    def __init__(self, **kwargs):
        self._business_date = None
        self._live = None
        self._live_timestamp = None
        self._securities = None
        super(RespSecurities, self).__init__(**kwargs)

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
    def securities(self):
        return self._securities

    @securities.setter
    def securities(self, value):
        self._assign("securities", value)


"""
$primary_keys(sec_isin)
"""


class RespSecuritiesSecurities(BaseContent):
    """
    """
    _swagger_types = {
        'basket_isin': 'BasketIsin',
        'currency': 'Currency',
        'iid': 'Iid',
        'margin_class_code': 'MarginClassCode',
        'price_unit': 'PriceUnit',
        'sec_id': 'SecId',
        'sec_isin': 'SecIsin',
        'sec_name': 'SecName',
        'sec_type': 'SecType',
        'security_mnemonic': 'SecurityMnemonic',
        'security_subtype': 'SecuritySubtype',
        'standard_settlement_period': 'StandardSettlementPeriod',
    }

    _default_values = {
        'basket_isin': False,
        'currency': 'EUR',
        'iid': 27471356,
        'margin_class_code': 'DB10',
        'price_unit': 'ABSOLUTE',
        'sec_id': 'DB1',
        'sec_isin': 'DE0005810055',
        'sec_name': 'DEUTSCHE BOERSE AG',
        'sec_type': 'SAKT',
        'security_mnemonic': 'DB1',
        'security_subtype': 'EQUITY',
        'standard_settlement_period': 2,
    }

    _primary_keys = ['sec_isin']

    def __init__(self, **kwargs):
        self._basket_isin = None
        self._currency = None
        self._iid = None
        self._margin_class_code = None
        self._price_unit = None
        self._sec_id = None
        self._sec_isin = None
        self._sec_name = None
        self._sec_type = None
        self._security_mnemonic = None
        self._security_subtype = None
        self._standard_settlement_period = None
        super(RespSecuritiesSecurities, self).__init__(**kwargs)

    @property
    def sec_id(self):
        return self._sec_id

    @sec_id.setter
    def sec_id(self, value):
        self._assign("sec_id", value)

    @property
    def sec_isin(self):
        return self._sec_isin

    @sec_isin.setter
    def sec_isin(self, value):
        self._assign("sec_isin", value)

    @property
    def sec_type(self):
        return self._sec_type

    @sec_type.setter
    def sec_type(self, value):
        self._assign("sec_type", value)

    @property
    def sec_name(self):
        return self._sec_name

    @sec_name.setter
    def sec_name(self, value):
        self._assign("sec_name", value)

    @property
    def iid(self):
        return self._iid

    @iid.setter
    def iid(self, value):
        self._assign("iid", value)

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        self._assign("currency", value)

    @property
    def security_mnemonic(self):
        return self._security_mnemonic

    @security_mnemonic.setter
    def security_mnemonic(self, value):
        self._assign("security_mnemonic", value)

    @property
    def standard_settlement_period(self):
        return self._standard_settlement_period

    @standard_settlement_period.setter
    def standard_settlement_period(self, value):
        self._assign("standard_settlement_period", value)

    @property
    def price_unit(self):
        return self._price_unit

    @price_unit.setter
    def price_unit(self, value):
        self._assign("price_unit", value)

    @property
    def security_subtype(self):
        return self._security_subtype

    @security_subtype.setter
    def security_subtype(self, value):
        self._assign("security_subtype", value)

    @property
    def margin_class_code(self):
        return self._margin_class_code

    @margin_class_code.setter
    def margin_class_code(self, value):
        self._assign("margin_class_code", value)

    @property
    def basket_isin(self):
        return self._basket_isin

    @basket_isin.setter
    def basket_isin(self, value):
        self._assign("basket_isin", value)
