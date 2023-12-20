from cpme_api.api.feature.models import BaseContent


"""
price unit, typically absolute for stocks and percentage for bonds
"""


class PriceUnit(BaseContent):

    _primitive = 'string'

    _enum = ['ABSOLUTE', 'PERCENTAGE']

    def __init__(self):
        self.example = 'ABSOLUTE'
