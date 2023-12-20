from cpme_api.api.feature.models import BaseContent


"""
Technical instrument ID. Needed for analytical requests - greeks, stress prices. If provided in request, all other key attributes are ignored
"""


class Iid(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = 27471356
