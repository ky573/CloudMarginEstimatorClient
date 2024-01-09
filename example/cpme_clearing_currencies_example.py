#!/usr/bin/env python
from cpme_api.api import CpmeApi, fancy, Configuration
from cpme_api.api.feature.utils import json_to_file

config = Configuration()
config.api_key = "9c40a29c-8b1d-4245-b3d9-2ffe5b5e9358"
config.url = "https://api.developer.deutsche-boerse.com/prisma-margin-estimator-2-0-2-0-0"
config.enable_logging = True
config.enable_pooling = True
config.return_json = True

api = CpmeApi(configuration=config)
res = api.clearing_currencies_get(live=True, verbose=True, async_req=False)
fancy(res, 'RESPONSE:')
json_to_file(res, "clearing_currencies")
api.close()