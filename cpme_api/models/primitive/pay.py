from cpme_api.api.feature.models import BaseContent


"""
pay leg, either Fixed rate or index plus optional spread
"""


class Pay(BaseContent):
    """
    """
    _primitive = 'string'

    def __init__(self):
        self.example = 'Fixed 0.15%'
