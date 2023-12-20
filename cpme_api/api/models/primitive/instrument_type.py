from cpme_api.api.feature.models import BaseContent


"""
Mandatory for flex, ignored otherwise
"""


class InstrumentType(BaseContent):

    _primitive = 'string'

    _enum = ['Future', 'Option', 'Flex Future', 'Flex Option']

    def __init__(self):
        self.example = 'Flex Option'
