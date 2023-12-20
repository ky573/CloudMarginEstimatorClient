from cpme_api.api.feature.models import BaseContent


"""
Exercise price for options, e.g. 10038.77. Empty for futures
"""


class ExercisePrice(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = 2400
