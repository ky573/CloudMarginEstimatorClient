from cpme_api.api.feature.models import BaseContent


"""
Is Cash Market available in the snapshot? Cash Market was introduced later to CPME and is not available for earlier snapshots. Live snapshots can be marked as cash_available which means Repo portfolio will be evaluated, however the Cash Market market data are from the first live snapshot of the day, not from the particular timestamp.
"""


class CashAvailable(BaseContent):
    """
    """
    _primitive = 'boolean'

    def __init__(self):
        self.example = None
