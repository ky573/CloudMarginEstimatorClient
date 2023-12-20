from cpme_api.api.feature.models import BaseContent


"""
security name, can be empty
"""


class SecName(BaseContent):

    _primitive = 'string'

    def __init__(self):
        self.example = 'DEUTSCHE BOERSE AG'
