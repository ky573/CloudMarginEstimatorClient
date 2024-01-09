from cpme_api.api.feature.models import BaseContent


"""
indicative margin for one product, long or short position $primary_keys(product_id)
"""


class ProductMarginLongShort(BaseContent):
    """
    """
    _swagger_types = {
        'im_components_long': 'ImComponents',
        'im_components_short': 'ImComponents',
        'liquidation_group': 'LiquidationGroup',
        'long_initial_margin': 'number',
        'long_initial_margin_cash': 'number',
        'margin_currency': 'Currency',
        'prod_name': 'string',
        'product_id': 'ProductId',
        'short_initial_margin': 'number',
        'short_initial_margin_cash': 'number',
    }

    _default_values = {
        'im_components_long': 'object',
        'im_components_short': 'object',
        'liquidation_group': 'None',
        'long_initial_margin': 'None',
        'long_initial_margin_cash': 'None',
        'margin_currency': 'EUR',
        'prod_name': 'None',
        'product_id': 'OESX',
        'short_initial_margin': 'None',
        'short_initial_margin_cash': 'None',
    }

    _primary_keys = ['product_id']

    def __init__(self, **kwargs):
        self._im_components_long = None
        self._im_components_short = None
        self._liquidation_group = None
        self._long_initial_margin = None
        self._long_initial_margin_cash = None
        self._margin_currency = None
        self._prod_name = None
        self._product_id = None
        self._short_initial_margin = None
        self._short_initial_margin_cash = None
        super(ProductMarginLongShort, self).__init__(**kwargs)

    @property
    def liquidation_group(self):
        return self._liquidation_group

    @liquidation_group.setter
    def liquidation_group(self, value):
        self._assign("liquidation_group", value)

    @property
    def product_id(self):
        return self._product_id

    @product_id.setter
    def product_id(self, value):
        self._assign("product_id", value)

    @property
    def prod_name(self):
        return self._prod_name

    @prod_name.setter
    def prod_name(self, value):
        self._assign("prod_name", value)

    @property
    def margin_currency(self):
        return self._margin_currency

    @margin_currency.setter
    def margin_currency(self, value):
        self._assign("margin_currency", value)

    @property
    def long_initial_margin(self):
        return self._long_initial_margin

    @long_initial_margin.setter
    def long_initial_margin(self, value):
        self._assign("long_initial_margin", value)

    @property
    def long_initial_margin_cash(self):
        return self._long_initial_margin_cash

    @long_initial_margin_cash.setter
    def long_initial_margin_cash(self, value):
        self._assign("long_initial_margin_cash", value)

    @property
    def short_initial_margin(self):
        return self._short_initial_margin

    @short_initial_margin.setter
    def short_initial_margin(self, value):
        self._assign("short_initial_margin", value)

    @property
    def short_initial_margin_cash(self):
        return self._short_initial_margin_cash

    @short_initial_margin_cash.setter
    def short_initial_margin_cash(self, value):
        self._assign("short_initial_margin_cash", value)

    @property
    def im_components_long(self):
        return self._im_components_long

    @im_components_long.setter
    def im_components_long(self, value):
        self._assign("im_components_long", value)

    @property
    def im_components_short(self):
        return self._im_components_short

    @im_components_short.setter
    def im_components_short(self, value):
        self._assign("im_components_short", value)
