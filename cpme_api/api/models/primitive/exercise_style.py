from cpme_api.api.feature.models import BaseContent


"""
Exercise style for options. Mandatory for Flex Option, ignored for standard options - product setup used
"""


class ExerciseStyle(BaseContent):

    _primitive = 'string'

    _enum = ['EUROPEAN', 'AMERICAN', '']

    def __init__(self):
        self.example = 'AMERICAN'
