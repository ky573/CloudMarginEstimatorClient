from cpme_api.api.feature.models import BaseContent


"""
Forward looking margin component for cash market, including margin grouping effect
"""


class AdditionalMargin(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = None
