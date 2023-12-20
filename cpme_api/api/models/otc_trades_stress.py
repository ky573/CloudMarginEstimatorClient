from cpme_api.api.feature.models import BaseContent


"""
Stress values on OTC trdae level, including short trade description. Internal Trade Id is used as a key. $primary_keys(trade_id)
"""


class OtcTradesStress(BaseContent):

    _swagger_types = {
        'ref': 'list[OtcTradesStressInner]',
    }

    def __init__(self):
        super(OtcTradesStress, self).__init__()
