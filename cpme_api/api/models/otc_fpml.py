from cpme_api.api.feature.models import BaseContent


"""
None
"""


class OtcFpml(BaseContent):

    _swagger_types = {
        'party': 'string',
        'xml': 'string',
    }

    _default_values = {
        'party': 'None',
        'xml': 'None',
    }

    _required = ['party', 'xml']

    def __init__(self, **kwargs):
        self._party = None
        self._xml = None
        super(OtcFpml, self).__init__(**kwargs)

    @property
    def party(self):
        return self._party

    @party.setter
    def party(self, value):
        self._assign("party", value)

    @property
    def xml(self):
        return self._xml

    @xml.setter
    def xml(self, value):
        self._assign("xml", value)
