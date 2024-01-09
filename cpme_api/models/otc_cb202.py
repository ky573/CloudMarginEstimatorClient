from cpme_api.api.feature.models import BaseContent


"""
None
"""


class OtcCb202(BaseContent):
    """
    """
    _swagger_types = {
        'account': 'string',
        'legal_entity': 'string',
        'member': 'string',
        'xml': 'string',
    }

    _default_values = {
        'account': 'None',
        'legal_entity': 'None',
        'member': 'None',
        'xml': 'None',
    }

    _required = ['xml']

    def __init__(self, **kwargs):
        self._account = None
        self._legal_entity = None
        self._member = None
        self._xml = None
        super(OtcCb202, self).__init__(**kwargs)

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
    def legal_entity(self):
        return self._legal_entity

    @legal_entity.setter
    def legal_entity(self, value):
        self._assign("legal_entity", value)

    @property
    def xml(self):
        return self._xml

    @xml.setter
    def xml(self, value):
        self._assign("xml", value)
