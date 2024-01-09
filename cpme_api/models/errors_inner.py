from cpme_api.api.feature.models import BaseContent


"""
None
"""


class ErrorsInner(BaseContent):
    """
    """
    _swagger_types = {
        'error_msg': 'string',
        'line_no': 'string',
        'portfolio': 'string',
    }

    _default_values = {
        'error_msg': 'None',
        'line_no': 'None',
        'portfolio': 'None',
    }

    _required = ['error_msg']

    def __init__(self, **kwargs):
        self._error_msg = None
        self._line_no = None
        self._portfolio = None
        super(ErrorsInner, self).__init__(**kwargs)

    @property
    def line_no(self):
        return self._line_no

    @line_no.setter
    def line_no(self, value):
        self._assign("line_no", value)

    @property
    def portfolio(self):
        return self._portfolio

    @portfolio.setter
    def portfolio(self, value):
        self._assign("portfolio", value)

    @property
    def error_msg(self):
        return self._error_msg

    @error_msg.setter
    def error_msg(self, value):
        self._assign("error_msg", value)
