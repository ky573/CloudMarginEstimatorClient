#!/usr/bin/env python
"""
Execute the script from ./example folder due to a relative path used in file name.

 Get attributes of securities (equities, bonds, subscription rights) for given ISIN, or all active securities known to the Risk system if ISIN is not specified.
 The margin class returned with the security is its default margin class and the currency is the default margin class currency. Bonds always have only one margin class, the default one. Equities may be assigned to multiple margin classes based on settlement currency of the transaction - this is intended for some ETFs.

  Parameters:
    QUERY PARAMETERS: 'business_date','live','live_timestamp','isin'

"""
from cpme_api.api import CpmeApi, Configuration
from cpme_api.api.feature.utils import json_to_file, list_to_csv

config = Configuration()
config.api_key = "9c40a29c-8b1d-4245-b3d9-2ffe5b5e9358"
config.enable_logging = True
config.proxy = 'http://webproxy.deutsche-boerse.de:8080'

api = CpmeApi(configuration=config)
sec = api.securities_get(isin='IT0003828271')
json_to_file(sec, file_name='./data/security')
list_to_csv(sec['securities'], './data/security')
sec = api.securities_get()
json_to_file(sec, file_name='./data/security_all')
list_to_csv(sec['securities'], './data/security_all')

api.close()
