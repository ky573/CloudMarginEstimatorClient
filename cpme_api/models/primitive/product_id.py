from cpme_api.api.feature.models import BaseContent


"""
Unique identifier of a product
"""


class ProductId(BaseContent):
    """
    """
    _primitive = 'string'

    def __init__(self):
        self.example = 'OESX'
