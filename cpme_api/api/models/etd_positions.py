from cpme_api.api.feature.models import BaseContent


"""
Margin figures on ETD position level. Full business key is used, it is not possible to map to input line_no one to one because positions may be aggregated or split. $primary_keys(iid,liquidation_group_split)
"""


class EtdPositions(BaseContent):

    _swagger_types = {
        'ref': 'list[EtdPositionsInner]',
    }

    def __init__(self):
        super(EtdPositions, self).__init__()
