from cpme_api.api.feature.models import BaseContent


"""
Exercised/Allocated minus Assigned/Notified balance
"""


class NetEa(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = 0
