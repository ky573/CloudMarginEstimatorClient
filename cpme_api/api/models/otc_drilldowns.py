from cpme_api.api.feature.models import BaseContent


"""
Margin figures and short trade desription on OTC trade level. Internal Trade Id is used as a key. $primary_keys(trade_id)
"""


class OtcDrilldowns(BaseContent):

    _swagger_types = {
        'ref': 'list[OtcDrilldownsInner]',
    }

    def __init__(self):
        super(OtcDrilldowns, self).__init__()
