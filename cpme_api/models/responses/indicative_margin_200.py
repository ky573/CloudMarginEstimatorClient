from cpme_api.api.feature.models import BaseContent


class IndicativeMargin200(BaseContent):
    """
    """
    one_of = [
        'SingleDateProductsMargin',
        'IndicativeMargin200Inner',
    ]

    primary_keys = ['business_date', 'live_timestamp']

