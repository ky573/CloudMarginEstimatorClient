from cpme_api.api.feature.models import BaseContent


"""
margin class code, up to 5 characters
"""


class MarginClassCode(BaseContent):
    """
    """
    _primitive = 'string'

    def __init__(self):
        self.example = 'DB10'
