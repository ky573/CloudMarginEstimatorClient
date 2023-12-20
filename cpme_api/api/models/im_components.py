from cpme_api.api.feature.models import BaseContent


"""
breakdown of initial margin to components
"""


class ImComponents(BaseContent):

    _swagger_types = {
        'liquidity_addon': 'LiquidityAddon',
        'long_option_credit': 'LongOptionCredit',
        'market_risk': 'MarketRisk',
        'market_risk_per_rms': 'list[ImComponentsMarketRiskPerRms]',
        'time_to_expiry_adjustment': 'TimeToExpiryAdjustment',
    }

    _default_values = {
        'liquidity_addon': 'None',
        'long_option_credit': 'None',
        'market_risk': 'None',
        'market_risk_per_rms': 'object',
        'time_to_expiry_adjustment': 'None',
    }

    def __init__(self, **kwargs):
        self._liquidity_addon = None
        self._long_option_credit = None
        self._market_risk = None
        self._market_risk_per_rms = None
        self._time_to_expiry_adjustment = None
        super(ImComponents, self).__init__(**kwargs)

    @property
    def market_risk(self):
        return self._market_risk

    @market_risk.setter
    def market_risk(self, value):
        self._assign("market_risk", value)

    @property
    def liquidity_addon(self):
        return self._liquidity_addon

    @liquidity_addon.setter
    def liquidity_addon(self, value):
        self._assign("liquidity_addon", value)

    @property
    def long_option_credit(self):
        return self._long_option_credit

    @long_option_credit.setter
    def long_option_credit(self, value):
        self._assign("long_option_credit", value)

    @property
    def time_to_expiry_adjustment(self):
        return self._time_to_expiry_adjustment

    @time_to_expiry_adjustment.setter
    def time_to_expiry_adjustment(self, value):
        self._assign("time_to_expiry_adjustment", value)

    @property
    def market_risk_per_rms(self):
        return self._market_risk_per_rms

    @market_risk_per_rms.setter
    def market_risk_per_rms(self, value):
        self._assign("market_risk_per_rms", value)


"""
breakdown for a particular risk measure set if the risk measure sets has multiple subsamples (obsolete), return mean value $primary_keys(rms_name)
"""


class ImComponentsMarketRiskPerRms(BaseContent):

    _swagger_types = {
        'compression_adjustment': 'CompressionAdjustment',
        'correlation_break_adjustment': 'CorrelationBreakAdjustment',
        'risk_measure_value': 'RiskMeasureValue',
        'rms_market_risk': 'RmsMarketRisk',
        'rms_name': 'RmsName',
        'simulation_type': 'SimulationType',
        'weighting_factor': 'WeightingFactor',
    }

    _default_values = {
        'compression_adjustment': 'None',
        'correlation_break_adjustment': 'None',
        'risk_measure_value': 'None',
        'rms_market_risk': 'None',
        'rms_name': 'None',
        'simulation_type': 'None',
        'weighting_factor': 'None',
    }

    _primary_keys = ['rms_name']

    def __init__(self, **kwargs):
        self._compression_adjustment = None
        self._correlation_break_adjustment = None
        self._risk_measure_value = None
        self._rms_market_risk = None
        self._rms_name = None
        self._simulation_type = None
        self._weighting_factor = None
        super(ImComponentsMarketRiskPerRms, self).__init__(**kwargs)

    @property
    def rms_name(self):
        return self._rms_name

    @rms_name.setter
    def rms_name(self, value):
        self._assign("rms_name", value)

    @property
    def simulation_type(self):
        return self._simulation_type

    @simulation_type.setter
    def simulation_type(self, value):
        self._assign("simulation_type", value)

    @property
    def weighting_factor(self):
        return self._weighting_factor

    @weighting_factor.setter
    def weighting_factor(self, value):
        self._assign("weighting_factor", value)

    @property
    def rms_market_risk(self):
        return self._rms_market_risk

    @rms_market_risk.setter
    def rms_market_risk(self, value):
        self._assign("rms_market_risk", value)

    @property
    def risk_measure_value(self):
        return self._risk_measure_value

    @risk_measure_value.setter
    def risk_measure_value(self, value):
        self._assign("risk_measure_value", value)

    @property
    def correlation_break_adjustment(self):
        return self._correlation_break_adjustment

    @correlation_break_adjustment.setter
    def correlation_break_adjustment(self, value):
        self._assign("correlation_break_adjustment", value)

    @property
    def compression_adjustment(self):
        return self._compression_adjustment

    @compression_adjustment.setter
    def compression_adjustment(self, value):
        self._assign("compression_adjustment", value)
