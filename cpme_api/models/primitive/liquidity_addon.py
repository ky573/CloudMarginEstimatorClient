from cpme_api.api.feature.models import BaseContent


"""
Liqu risk from ReportCP046
"""


class LiquidityAddon(BaseContent):
    """
    """
    _primitive = 'number'

    def __init__(self):
        self.example = None
