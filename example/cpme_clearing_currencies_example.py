#!/usr/bin/env python
"""
List of clearing currencies that can be used in /estimator request.

The example shows and save result into the json file.
"""
from cpme_api.api import CpmeApi, fancy, Configuration
from cpme_api.api.feature.utils import json_to_file

config = Configuration()
config.api_key = "9c40a29c-8b1d-4245-b3d9-2ffe5b5e9358"
config.enable_logging = True
config.proxy = 'http://webproxy.deutsche-boerse.de:8080'

api = CpmeApi(configuration=config)
res = api.clearing_currencies_get(live=True, verbose=True, request_timeout=5)
fancy(res, 'RESPONSE:')
# json_to_file(res, "clearing_currencies")
api.close()
