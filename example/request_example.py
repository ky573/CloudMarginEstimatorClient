#!/usr/bin/env python
"""
This is simple example with standard requests library which send the request to /indicative_margin and
save the results into the excel sheet.
"""
import requests


PARAMS = {
    'clearing_house': 'EUXCDEFF',
    'products': ['FDAX', 'CONF'],
    'format': 'XLSX',
    'business_date': '20220623'
}

DEFAULT_PARAMS = {}

API_KEY = '9c40a29c-8b1d-4245-b3d9-2ffe5b5e9358'

HEADER = {'Content-Type': 'application/json', 'X-DBP-APIKEY': API_KEY}

URL = 'https://api.developer.deutsche-boerse.com/prod/prisma-margin-estimator-2-0/2.0.0'

EP = '/indicative_margin'

response = requests.get(URL + EP,
                        params=PARAMS,
                        headers=HEADER)

if 'Content-Type' in response.headers:
    if 'sheet' in response.headers["Content-Type"]:
        with open(f'result_im.xlsx', 'wb') as stream:
            stream.write(response.content)
else:
    print(response.json())
