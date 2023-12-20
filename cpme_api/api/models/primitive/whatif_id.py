from cpme_api.api.feature.models import BaseContent


"""
id of the what-if scenario - marks the portfolio components that should be part of the scenario (on top on the base portfolio components, which are not labeled by whatif_id or have whatif_id=0) and marks the resulting portfolio margin for the scenario
"""


class WhatifId(BaseContent):

    _primitive = 'number'

    def __init__(self):
        self.example = 1
