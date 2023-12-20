from cpme_api.api.feature.models import BaseContent


"""
Compression Adjustment for this RMS
"""


class CompressionAdjustment(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = None
