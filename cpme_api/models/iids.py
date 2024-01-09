from cpme_api.api.feature.models import BaseContent


"""
Technical ids of instruments, see series resource
"""


class Iids(BaseContent):
    """
    """
    _swagger_types = {
        'ref': 'list[IidsInner]',
    }

    def __init__(self):
        super(Iids, self).__init__()
