from cpme_api.api.feature.models import BaseContent


"""
Line number, used when reporting errors or position-level results
"""


class LineNo(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = 1
