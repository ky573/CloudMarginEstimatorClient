from cpme_api.api.feature.models import BaseContent


"""
array with indicative margins for a selected date range $primary_keys(business_date,live_timestamp)
"""


class IndicativeMargin200Inner(BaseContent):
    """
    """
    _swagger_types = {
        'ref': 'list[SingleDateProductsMargin]',
    }

    def __init__(self):
        super(IndicativeMargin200Inner, self).__init__()
