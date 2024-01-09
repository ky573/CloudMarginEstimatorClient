from cpme_api.api.feature.models import BaseContent


"""
EurexOTC CC233 report with information which member/account should be selected from the report
"""


class OtcCc233(BaseContent):
    """
    """
    _swagger_types = {
        'account': 'string',
        'csv': 'string',
        'member': 'string',
    }

    _default_values = {
        'account': 'None',
        'csv': """Value Date: 2021-05-31
Book,TradeID,TradeStatus,MaturityDate,ProductType,ExtendedProductType,TradeCurrency,Principal,PrincipalAmountPay,PrincipalAmountRec,ProductDescription,FinalReferenceDate,MarketDataItem,CurveType,CurveTenor,Bucket,DeltaSensitivity,Risk_Netting_Unit
XYZFR_A1,1,VERIFIED,23/04/2032,Swap,Swap,EUR,2500000,2500000,2500000,Swap/04/23/2032/P:EUR 0.03000 /R:EUR/EURIBOR/6M,,DIS EUR ESTR ZC OFFICIAL,CurveZero,1D,3Y,2.03,""",
        'member': 'None',
    }

    _required = ['member', 'account', 'csv']

    def __init__(self, **kwargs):
        self._account = None
        self._csv = None
        self._member = None
        super(OtcCc233, self).__init__(**kwargs)

    @property
    def member(self):
        return self._member

    @member.setter
    def member(self, value):
        self._assign("member", value)

    @property
    def account(self):
        return self._account

    @account.setter
    def account(self, value):
        self._assign("account", value)

    @property
    def csv(self):
        return self._csv

    @csv.setter
    def csv(self, value):
        self._assign("csv", value)
