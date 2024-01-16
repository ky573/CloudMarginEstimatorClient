#!/usr/bin/env python
"""
Execute the script from ./example folder due to a relative path used in file name.

List of end-of-day or first live snapshots that can be used in other requests.

The example shows and save result into the json file.
"""
from cpme_api.api import CpmeApi, Configuration, fancy
from cpme_api.api.feature.utils import json_to_file


config = Configuration()
config.api_key = "9c40a29c-8b1d-4245-b3d9-2ffe5b5e9358"
config.enable_logging = True
config.proxy = 'http://webproxy.deutsche-boerse.de:8080'

api = CpmeApi(configuration=config)
resp = api.snapshots_get(business_date=20230110)
fancy(resp)
# json_to_file(resp, './data/snapshots')
api.close()