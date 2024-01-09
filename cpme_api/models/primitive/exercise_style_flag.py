from cpme_api.api.feature.models import BaseContent


"""
E for European, A for American, empty for futures; can differ from product exercise style for Flex Option
"""


class ExerciseStyleFlag(BaseContent):
    """
    """
    _primitive = 'string'

    _enum = ['E', 'A', '']

    def __init__(self):
        self.example = 'A'
