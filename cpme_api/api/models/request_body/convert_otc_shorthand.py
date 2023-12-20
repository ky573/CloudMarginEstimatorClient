from cpme_api.api.feature.models import BaseContent


"""
None
"""


class BodyConvertOtcShorthand(BaseContent):

    _swagger_types = {
        'otc_shorthand_lines': 'string',
    }

    _default_values = {
        'otc_shorthand_lines': 'USD 200m 10Y pay 1.5%',
    }

    _required = ['otc_shorthand_lines']

    def __init__(self, **kwargs):
        self._otc_shorthand_lines = None
        super(BodyConvertOtcShorthand, self).__init__(**kwargs)

    @property
    def otc_shorthand_lines(self):
        return self._otc_shorthand_lines

    @otc_shorthand_lines.setter
    def otc_shorthand_lines(self, value):
        self._assign("otc_shorthand_lines", value)
