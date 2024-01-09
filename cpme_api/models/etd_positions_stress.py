from cpme_api.api.feature.models import BaseContent


"""
Stress values ETD position level. Full business key is used, it is not possible to map to input line_no one to one because positions may be aggregated or split.
"""


class EtdPositionsStress(BaseContent):
    """
    """
    _swagger_types = {
        'ref': 'list[EtdPositionsStressInner]',
    }

    def __init__(self):
        super(EtdPositionsStress, self).__init__()
