from cpme_api.api.feature.models import BaseContent


"""
$primary_keys(line_no,leg_type)
"""


class CashJson(BaseContent):
    """
    """
    _swagger_types = {
        'ref': 'list[CashJsonPosition]',
    }

    def __init__(self):
        super(CashJson, self).__init__()
