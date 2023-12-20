from cpme_api.api.feature.models import BaseContent


"""
Greek types, array with the following valid values
"""


class GreekTypes(BaseContent):

    _swagger_types = {
        'ref': 'list[GreekTypesInner]',
    }

    def __init__(self):
        super(GreekTypes, self).__init__()
