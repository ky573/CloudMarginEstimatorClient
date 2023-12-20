from cpme_api.api.feature.models import BaseContent


"""
Vector of underlying price shifts, optional. If not given then the current underlying price is used
"""


class UnderlyingShiftsRel(BaseContent):

    _swagger_types = {
        'ref': 'list[UnderlyingShiftsRelInner]',
    }

    def __init__(self):
        super(UnderlyingShiftsRel, self).__init__()
