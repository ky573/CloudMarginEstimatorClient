from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespGlobalScenarios(BaseContent):
    """
    """
    _swagger_types = {
        'business_date': 'BusinessDate',
        'live': 'Live',
        'live_timestamp': 'LiveTimestamp',
        'scenarios': 'list[RespGlobalScenariosScenarios]',
    }

    _default_values = {
        'business_date': '20181205',
        'live': False,
        'live_timestamp': 0,
        'scenarios': 'object',
    }

    def __init__(self, **kwargs):
        self._business_date = None
        self._live = None
        self._live_timestamp = None
        self._scenarios = None
        super(RespGlobalScenarios, self).__init__(**kwargs)

    @property
    def business_date(self):
        return self._business_date

    @business_date.setter
    def business_date(self, value):
        self._assign("business_date", value)

    @property
    def live(self):
        return self._live

    @live.setter
    def live(self, value):
        self._assign("live", value)

    @property
    def live_timestamp(self):
        return self._live_timestamp

    @live_timestamp.setter
    def live_timestamp(self, value):
        self._assign("live_timestamp", value)

    @property
    def scenarios(self):
        return self._scenarios

    @scenarios.setter
    def scenarios(self, value):
        self._assign("scenarios", value)


"""
$primary_keys(gscnid)
"""


class RespGlobalScenariosScenarios(BaseContent):
    """
    """
    _swagger_types = {
        'global_scenario': 'GlobalScenario',
        'gscnid': 'Gscnid',
    }

    _default_values = {
        'global_scenario': 'Lehman crash 15.09.2008',
        'gscnid': 1,
    }

    _primary_keys = ['gscnid']

    def __init__(self, **kwargs):
        self._global_scenario = None
        self._gscnid = None
        super(RespGlobalScenariosScenarios, self).__init__(**kwargs)

    @property
    def global_scenario(self):
        return self._global_scenario

    @global_scenario.setter
    def global_scenario(self, value):
        self._assign("global_scenario", value)

    @property
    def gscnid(self):
        return self._gscnid

    @gscnid.setter
    def gscnid(self, value):
        self._assign("gscnid", value)
