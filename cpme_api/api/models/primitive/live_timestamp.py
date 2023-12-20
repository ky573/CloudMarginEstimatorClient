from cpme_api.api.feature.models import BaseContent


"""
Timestamp as of which the result is calculated, in milliseconds from epoch. Zero means first live snapshot of the day.
"""


class LiveTimestamp(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = 0
