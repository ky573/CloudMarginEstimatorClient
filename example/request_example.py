#!/usr/bin/env python
"""
This is simple example with standard requests library which send the request to /indicative_margin and
save the results into the excel sheet.
"""
import requests


PARAMS = {
    'clearing_house': 'EUXCDEFF',  # 'EUXCDEFF' or 'EEXCDE8L'
    'products': ['RFVO', 'RFSX'],
    'format': 'XLSX',  # JSON, XLS, XLSX
    'business_date': '20220623'
}

DEFAULT_PARAMS = {}

API_KEY = 'b953e6e4-235e-4217-a7b0-ceb071a9dba1'

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
