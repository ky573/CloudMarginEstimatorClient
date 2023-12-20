from cpme_api.api.feature.models import BaseContent


"""
None
"""


class BodyConvertEtdCp005(BaseContent):

    _swagger_types = {
        'account': 'string',
        'member': 'string',
        'xml': 'string',
    }

    _default_values = {
        'account': 'None',
        'member': 'None',
        'xml': 'None',
    }

    _required = ['xml']

    def __init__(self, **kwargs):
        self._account = None
        self._member = None
        self._xml = None
        super(BodyConvertEtdCp005, self).__init__(**kwargs)

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
    def xml(self):
        return self._xml

    @xml.setter
    def xml(self, value):
        self._assign("xml", value)
