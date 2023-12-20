from cpme_api.api.feature.models import BaseContent


"""
Time to Expiry Adjustment a.k.a. TEA from ReportCP046, introduced with Prisma R8.0
"""


class TimeToExpiryAdjustment(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = None
