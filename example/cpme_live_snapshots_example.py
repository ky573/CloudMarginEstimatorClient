#!/usr/bin/env python
"""
List of live (intraday) snapshots for given business_date..
"""
import ipdb

from cpme_api.api import CpmeApi, Configuration
from cpme_api.api.feature.utils import json_to_file


config = Configuration()
config.api_key = "9c40a29c-8b1d-4245-b3d9-2ffe5b5e9358"
# config.url = "https://risk.developer.deutsche-boerse.com/prisma-margin-estimator-2-0-2-0-0"
# config.enable_logging = False
config.proxy = 'http://webproxy.deutsche-boerse.de:8080'
config.enable_pooling = True
log = config.get_loggger()

api = CpmeApi(configuration=config)

ipdb.set_trace()
resp = api.live_snapshots_get(async_req=True, business_date=20230110)
json_to_file(resp, 'llllive_snapshots')
api.close()
