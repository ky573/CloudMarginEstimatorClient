from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespProducts(BaseContent):

    _swagger_types = {
        'business_date': 'BusinessDate',
        'live': 'Live',
        'live_timestamp': 'LiveTimestamp',
        'products': 'list[RespProductsProducts]',
    }

    _default_values = {
        'business_date': '20181205',
        'live': False,
        'live_timestamp': 0,
        'products': 'object',
    }

    def __init__(self, **kwargs):
        self._business_date = None
        self._live = None
        self._live_timestamp = None
        self._products = None
        super(RespProducts, self).__init__(**kwargs)

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
    def products(self):
        return self._products

    @products.setter
    def products(self, value):
        self._assign("products", value)


"""
None
"""


class RespProductsProducts(BaseContent):

    _swagger_types = {
        'clearing_house': 'string',
        'currency': 'Currency',
        'exercise_style_flag': 'ExerciseStyleFlag',
        'extended_product_type': 'string',
        'final_settlement_time': 'string',
        'instrument_type': 'string',
        'liquidation_group': 'LiquidationGroup',
        'margin_style_flag': 'string',
        'prod_isin': 'string',
        'prod_name': 'string',
        'product': 'ProductId',
        'product_settlement_type': 'string',
        'product_tick_size': 'number',
        'product_tick_value': 'number',
        'product_type': 'string',
        'underlying_isin': 'string',
        'xm_eligibility': 'boolean',
    }

    _default_values = {
        'clearing_house': 'None',
        'currency': 'EUR',
        'exercise_style_flag': 'A',
        'extended_product_type': 'None',
        'final_settlement_time': 'None',
        'instrument_type': 'None',
        'liquidation_group': 'None',
        'margin_style_flag': 'None',
        'prod_isin': 'None',
        'prod_name': 'None',
        'product': 'OESX',
        'product_settlement_type': 'None',
        'product_tick_size': 'None',
        'product_tick_value': 'None',
        'product_type': 'None',
        'underlying_isin': 'None',
        'xm_eligibility': 'None',
    }

    _required = ['product', 'instrument_type']

    def __init__(self, **kwargs):
        self._clearing_house = None
        self._currency = None
        self._exercise_style_flag = None
        self._extended_product_type = None
        self._final_settlement_time = None
        self._instrument_type = None
        self._liquidation_group = None
        self._margin_style_flag = None
        self._prod_isin = None
        self._prod_name = None
        self._product = None
        self._product_settlement_type = None
        self._product_tick_size = None
        self._product_tick_value = None
        self._product_type = None
        self._underlying_isin = None
        self._xm_eligibility = None
        super(RespProductsProducts, self).__init__(**kwargs)

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, value):
        self._assign("product", value)

    @property
    def instrument_type(self):
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, value):
        self._assign("instrument_type", value)

    @property
    def clearing_house(self):
        return self._clearing_house

    @clearing_house.setter
    def clearing_house(self, value):
        self._assign("clearing_house", value)

    @property
    def prod_name(self):
        return self._prod_name

    @prod_name.setter
    def prod_name(self, value):
        self._assign("prod_name", value)

    @property
    def prod_isin(self):
        return self._prod_isin

    @prod_isin.setter
    def prod_isin(self, value):
        self._assign("prod_isin", value)

    @property
    def underlying_isin(self):
        return self._underlying_isin

    @underlying_isin.setter
    def underlying_isin(self, value):
        self._assign("underlying_isin", value)

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        self._assign("currency", value)

    @property
    def product_type(self):
        return self._product_type

    @product_type.setter
    def product_type(self, value):
        self._assign("product_type", value)

    @property
    def extended_product_type(self):
        return self._extended_product_type

    @extended_product_type.setter
    def extended_product_type(self, value):
        self._assign("extended_product_type", value)

    @property
    def margin_style_flag(self):
        return self._margin_style_flag

    @margin_style_flag.setter
    def margin_style_flag(self, value):
        self._assign("margin_style_flag", value)

    @property
    def exercise_style_flag(self):
        return self._exercise_style_flag

    @exercise_style_flag.setter
    def exercise_style_flag(self, value):
        self._assign("exercise_style_flag", value)

    @property
    def product_settlement_type(self):
        return self._product_settlement_type

    @product_settlement_type.setter
    def product_settlement_type(self, value):
        self._assign("product_settlement_type", value)

    @property
    def final_settlement_time(self):
        return self._final_settlement_time

    @final_settlement_time.setter
    def final_settlement_time(self, value):
        self._assign("final_settlement_time", value)

    @property
    def product_tick_size(self):
        return self._product_tick_size

    @product_tick_size.setter
    def product_tick_size(self, value):
        self._assign("product_tick_size", value)

    @property
    def product_tick_value(self):
        return self._product_tick_value

    @product_tick_value.setter
    def product_tick_value(self, value):
        self._assign("product_tick_value", value)

    @property
    def liquidation_group(self):
        return self._liquidation_group

    @liquidation_group.setter
    def liquidation_group(self, value):
        self._assign("liquidation_group", value)

    @property
    def xm_eligibility(self):
        return self._xm_eligibility

    @xm_eligibility.setter
    def xm_eligibility(self, value):
        self._assign("xm_eligibility", value)
