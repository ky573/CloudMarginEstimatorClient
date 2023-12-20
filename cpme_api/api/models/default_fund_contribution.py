from cpme_api.api.feature.models import BaseContent


"""
Estimated contribution to the Default Fund for submitted portfolio, based on the worst global scenario
"""


class DefaultFundContribution(BaseContent):

    _swagger_types = {
        'currency': 'ClearingCurrency',
        'default_fund_requirement': 'DefaultFundRequirement',
        'slom_drilldown': 'list[DefaultFundContributionSlomDrilldown]',
        'stress_loss_over_margin': 'StressLossOverMargin',
        'worst_global_scenario': 'GlobalScenario',
    }

    _default_values = {
        'currency': 'EUR',
        'default_fund_requirement': 16634756,
        'slom_drilldown': 'object',
        'stress_loss_over_margin': -101808201.0,
        'worst_global_scenario': 'Lehman crash 15.09.2008',
    }

    def __init__(self, **kwargs):
        self._currency = None
        self._default_fund_requirement = None
        self._slom_drilldown = None
        self._stress_loss_over_margin = None
        self._worst_global_scenario = None
        super(DefaultFundContribution, self).__init__(**kwargs)

    @property
    def worst_global_scenario(self):
        return self._worst_global_scenario

    @worst_global_scenario.setter
    def worst_global_scenario(self, value):
        self._assign("worst_global_scenario", value)

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        self._assign("currency", value)

    @property
    def stress_loss_over_margin(self):
        return self._stress_loss_over_margin

    @stress_loss_over_margin.setter
    def stress_loss_over_margin(self, value):
        self._assign("stress_loss_over_margin", value)

    @property
    def default_fund_requirement(self):
        return self._default_fund_requirement

    @default_fund_requirement.setter
    def default_fund_requirement(self, value):
        self._assign("default_fund_requirement", value)

    @property
    def slom_drilldown(self):
        return self._slom_drilldown

    @slom_drilldown.setter
    def slom_drilldown(self, value):
        self._assign("slom_drilldown", value)


"""
Result of the global scenario $primary_keys(global_scenario)
"""


class DefaultFundContributionSlomDrilldown(BaseContent):

    _swagger_types = {
        'global_scenario': 'GlobalScenario',
        'slom_per_lg_mg': 'list[DefaultFundContributionSlomPerLgMg]',
        'stress_loss_over_margin': 'StressLossOverMargin',
        'stress_value': 'StressValue',
        'total_margin_requirement': 'TotalMarginRequirement',
    }

    _default_values = {
        'global_scenario': 'Lehman crash 15.09.2008',
        'slom_per_lg_mg': 'object',
        'stress_loss_over_margin': -101808201.0,
        'stress_value': -107168880.0,
        'total_margin_requirement': 5362113.0,
    }

    _primary_keys = ['global_scenario']

    def __init__(self, **kwargs):
        self._global_scenario = None
        self._slom_per_lg_mg = None
        self._stress_loss_over_margin = None
        self._stress_value = None
        self._total_margin_requirement = None
        super(DefaultFundContributionSlomDrilldown, self).__init__(**kwargs)

    @property
    def global_scenario(self):
        return self._global_scenario

    @global_scenario.setter
    def global_scenario(self, value):
        self._assign("global_scenario", value)

    @property
    def stress_value(self):
        return self._stress_value

    @stress_value.setter
    def stress_value(self, value):
        self._assign("stress_value", value)

    @property
    def total_margin_requirement(self):
        return self._total_margin_requirement

    @total_margin_requirement.setter
    def total_margin_requirement(self, value):
        self._assign("total_margin_requirement", value)

    @property
    def stress_loss_over_margin(self):
        return self._stress_loss_over_margin

    @stress_loss_over_margin.setter
    def stress_loss_over_margin(self, value):
        self._assign("stress_loss_over_margin", value)

    @property
    def slom_per_lg_mg(self):
        return self._slom_per_lg_mg

    @slom_per_lg_mg.setter
    def slom_per_lg_mg(self, value):
        self._assign("slom_per_lg_mg", value)


"""
Result for the Liquidation Group (if ETD) or the Margin Group (if Cash Market) in given global scenario. Either the liquidation_group or margin_group is filled. Margin Classes that do not belong to a Margin Group are listed on this level as well and their margin_group_code is equal to margin_class_code prefixed by '!'. $primary_keys(liquidation_group,margin_group_code)
"""


class DefaultFundContributionSlomPerLgMg(BaseContent):

    _swagger_types = {
        'liquidation_group': 'LiquidationGroup',
        'margin_group_code': 'MarginGroupCode',
        'slom_per_lgs_mc': 'list[DefaultFundContributionSlomPerLgsMc]',
        'stress_loss_over_margin': 'StressLossOverMargin',
        'stress_value_liquidity_risk': 'StressValueLiquidityRisk',
        'stress_value_market_risk': 'StressValueMarketRisk',
        'total_margin_requirement': 'TotalMarginRequirement',
    }

    _default_values = {
        'liquidation_group': 'None',
        'margin_group_code': 'None',
        'slom_per_lgs_mc': 'object',
        'stress_loss_over_margin': -101808201.0,
        'stress_value_liquidity_risk': -1310.0,
        'stress_value_market_risk': -107168880.0,
        'total_margin_requirement': 5362113.0,
    }

    _primary_keys = ['liquidation_group', 'margin_group_code']

    def __init__(self, **kwargs):
        self._liquidation_group = None
        self._margin_group_code = None
        self._slom_per_lgs_mc = None
        self._stress_loss_over_margin = None
        self._stress_value_liquidity_risk = None
        self._stress_value_market_risk = None
        self._total_margin_requirement = None
        super(DefaultFundContributionSlomPerLgMg, self).__init__(**kwargs)

    @property
    def liquidation_group(self):
        return self._liquidation_group

    @liquidation_group.setter
    def liquidation_group(self, value):
        self._assign("liquidation_group", value)

    @property
    def margin_group_code(self):
        return self._margin_group_code

    @margin_group_code.setter
    def margin_group_code(self, value):
        self._assign("margin_group_code", value)

    @property
    def stress_value_market_risk(self):
        return self._stress_value_market_risk

    @stress_value_market_risk.setter
    def stress_value_market_risk(self, value):
        self._assign("stress_value_market_risk", value)

    @property
    def stress_value_liquidity_risk(self):
        return self._stress_value_liquidity_risk

    @stress_value_liquidity_risk.setter
    def stress_value_liquidity_risk(self, value):
        self._assign("stress_value_liquidity_risk", value)

    @property
    def total_margin_requirement(self):
        return self._total_margin_requirement

    @total_margin_requirement.setter
    def total_margin_requirement(self, value):
        self._assign("total_margin_requirement", value)

    @property
    def stress_loss_over_margin(self):
        return self._stress_loss_over_margin

    @stress_loss_over_margin.setter
    def stress_loss_over_margin(self, value):
        self._assign("stress_loss_over_margin", value)

    @property
    def slom_per_lgs_mc(self):
        return self._slom_per_lgs_mc

    @slom_per_lgs_mc.setter
    def slom_per_lgs_mc(self, value):
        self._assign("slom_per_lgs_mc", value)


"""
Result for the Liquidation Group Split or Margin Class. $primary_keys(liquidation_group_split)
"""


class DefaultFundContributionSlomPerLgsMc(BaseContent):

    _swagger_types = {
        'liquidation_group_split': 'LiquidationGroupSplit',
        'margin_class_code': 'MarginClassCode',
        'stress_loss_over_margin': 'StressLossOverMargin',
        'stress_value_liquidity_risk': 'StressValueLiquidityRisk',
        'stress_value_market_risk': 'StressValueMarketRisk',
        'total_margin_requirement': 'TotalMarginRequirement',
        'worst_system_scnid': 'number',
    }

    _default_values = {
        'liquidation_group_split': 'None',
        'margin_class_code': 'DB10',
        'stress_loss_over_margin': -101808201.0,
        'stress_value_liquidity_risk': -1310.0,
        'stress_value_market_risk': -107168880.0,
        'total_margin_requirement': 5362113.0,
        'worst_system_scnid': 'None',
    }

    _primary_keys = ['liquidation_group_split']

    def __init__(self, **kwargs):
        self._liquidation_group_split = None
        self._margin_class_code = None
        self._stress_loss_over_margin = None
        self._stress_value_liquidity_risk = None
        self._stress_value_market_risk = None
        self._total_margin_requirement = None
        self._worst_system_scnid = None
        super(DefaultFundContributionSlomPerLgsMc, self).__init__(**kwargs)

    @property
    def liquidation_group_split(self):
        return self._liquidation_group_split

    @liquidation_group_split.setter
    def liquidation_group_split(self, value):
        self._assign("liquidation_group_split", value)

    @property
    def margin_class_code(self):
        return self._margin_class_code

    @margin_class_code.setter
    def margin_class_code(self, value):
        self._assign("margin_class_code", value)

    @property
    def stress_value_market_risk(self):
        return self._stress_value_market_risk

    @stress_value_market_risk.setter
    def stress_value_market_risk(self, value):
        self._assign("stress_value_market_risk", value)

    @property
    def stress_value_liquidity_risk(self):
        return self._stress_value_liquidity_risk

    @stress_value_liquidity_risk.setter
    def stress_value_liquidity_risk(self, value):
        self._assign("stress_value_liquidity_risk", value)

    @property
    def total_margin_requirement(self):
        return self._total_margin_requirement

    @total_margin_requirement.setter
    def total_margin_requirement(self, value):
        self._assign("total_margin_requirement", value)

    @property
    def stress_loss_over_margin(self):
        return self._stress_loss_over_margin

    @stress_loss_over_margin.setter
    def stress_loss_over_margin(self, value):
        self._assign("stress_loss_over_margin", value)

    @property
    def worst_system_scnid(self):
        return self._worst_system_scnid

    @worst_system_scnid.setter
    def worst_system_scnid(self, value):
        self._assign("worst_system_scnid", value)
