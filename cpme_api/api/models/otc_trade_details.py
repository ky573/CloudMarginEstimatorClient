from cpme_api.api.feature.models import BaseContent


"""
None
"""


class OtcTradeDetails(BaseContent):

    _swagger_types = {
        'ref': 'list[OtcTradeDetailsInner]',
    }

    def __init__(self):
        super(OtcTradeDetails, self).__init__()
