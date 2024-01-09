#!/usr/bin/env python
from cpme_api.api import CpmeApi, fancy, Configuration
from cpme_api.api.feature.utils import json_to_file

config = Configuration()
config.api_key = "afafsdfdsfsfds"
config.enable_logging = True
config.enable_pooling = True
config.return_json = True

api = CpmeApi(configuration=config)
res = api.clearing_currencies_get(live=True, verbose=True, async_req=False)
fancy(res, 'RESPONSE:')
json_to_file(res, "clearing_currencies")
api.close()
