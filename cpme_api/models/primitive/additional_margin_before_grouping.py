from cpme_api.api.feature.models import BaseContent


"""
Forward looking margin component for cash market, as if there was no margin grouping
"""


class AdditionalMarginBeforeGrouping(BaseContent):
    """
    """
    _primitive = 'number'

    def __init__(self):
        self.example = None
