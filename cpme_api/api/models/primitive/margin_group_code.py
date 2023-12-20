from cpme_api.api.feature.models import BaseContent


"""
Margin group that the margin class is assigned to. Can be empty, that means no grouping
"""


class MarginGroupCode(BaseContent):

    _primitive = 'string'

    def __init__(self):
        self.example = None
