from cpme_api.api.feature.models import BaseContent


"""
Is OTC available in the snapshot? Snapshot can exist without OTC, then only ETD portfolio can be evaluated. Snapshot without ETD is not possible. Live snapshots can be marked as otc_available which means OTC portfolio will be evaluated, however the OTC market data are from first live snapshot of the day, not from the particular timestamp.
"""


class OtcAvailable(BaseContent):
    """
    """
    _primitive = 'boolean'

    def __init__(self):
        self.example = True
