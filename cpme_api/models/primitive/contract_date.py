from cpme_api.api.feature.models import BaseContent


"""
Contract date of the instrument in YYYYMMDD format. Introduced with Next Generation ETD contracts initiative as part of the series primary key. Maturity (meaning contract_maturity) can still be used alternatives to contract_date, however only contract_date guarantees uniqueness.
"""


class ContractDate(BaseContent):
    """
    """
    _primitive = 'number'

    def __init__(self):
        self.example = 20281215
