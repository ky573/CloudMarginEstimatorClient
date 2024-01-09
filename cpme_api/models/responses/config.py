from cpme_api.api.feature.models import BaseContent


"""
None
"""


class RespConfig(BaseContent):
    """
    """
    _swagger_types = {
        'max_body_size': 'number',
    }

    _default_values = {
        'max_body_size': 'None',
    }

    def __init__(self, **kwargs):
        self._max_body_size = None
        super(RespConfig, self).__init__(**kwargs)

    @property
    def max_body_size(self):
        return self._max_body_size

    @max_body_size.setter
    def max_body_size(self, value):
        self._assign("max_body_size", value)
