from cpme_api.api.feature.models import BaseContent


"""
Is the snapshot live (a.k.a. intraday)? False for end-of-day. In request, False without any date means last end-of-day.
"""


class Live(BaseContent):
    """
    """
    _primitive = 'boolean'

    def __init__(self):
        self.example = False
