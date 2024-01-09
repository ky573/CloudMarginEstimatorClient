from cpme_api.api.feature.models import BaseContent


"""
Internal value used by Prisma
"""


class ExpiryMaturity(BaseContent):
    """
    """
    _primitive = 'number'

    def __init__(self):
        self.example = 202812
