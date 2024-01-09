from cpme_api.api.feature.models import BaseContent


"""
$primary_keys(line_no)
"""


class RepoJson(BaseContent):
    """
    """
    _swagger_types = {
        'ref': 'list[RepoJsonPosition]',
    }

    def __init__(self):
        super(RepoJson, self).__init__()
