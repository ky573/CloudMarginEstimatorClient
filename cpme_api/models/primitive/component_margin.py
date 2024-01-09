from cpme_api.api.feature.models import BaseContent


"""
Initial margin on position level is a approximation based on compVaR. compVaR is calculated to split VaR among positions, then other add-ons are added proportionally to compVaR
"""


class ComponentMargin(BaseContent):
    """
    """
    _primitive = 'number'

    def __init__(self):
        self.example = None
