#!/usr/bin/env python
"""
Execute the script from ./example folder due to a relative path used in file name.

Get indicative margin for one future contract (front month contract of given future product) in EUR. By default all Eurex futures are included,
unless ECC clearing house is selected or a specific product or products is requested. The resulting long_initial_margin_cash and short_initial_margin_cash
is equivalent to the margin calculated by individual /estimator requests for portfolio of one long or short contract, respectively.
The relative long_initial_margin and short_initial_margin is the cash margin divided by (current underlying price converted to EUR * trade unit value).
Optionally business date can be specified to get historical indicative margins, by default CPME returns the most recent values.
In contrast to estimator request, which uses end-of-day for historical calculation (unless time is specified),
indicative margin is by default for the first live snapshot (published in the morning to indicate margin during the day).

Time Range
As an alternative to selecting one business_date, time series can be requested using business_date_from, business_date_to attributes. This is available only for JSON output format.

  Parameters:
    QUERY PARAMETERS: 'clearing_house','products','format','business_date','business_date_from','business_date_to','live','include_components'

"""
from cpme_api.api import CpmeApi, fancy, Configuration
from cpme_api.api.tools import get_business_date
from cpme_api.api.feature.utils import json_to_file


config = Configuration()
config.api_key = "9c40a29c-8b1d-4245-b3d9-2ffe5b5e9358"
config.enable_logging = True
log = config.get_loggger()
config.proxy = 'http://webproxy.deutsche-boerse.de:8080'


def save_to_excel(api_: CpmeApi, p: dict):
    fancy(p, 'QUERY_PARAMS:')
    resp = api.indicative_margin_get(**p, verbose=True)
    if 'Content-Type' in resp.headers:
        if 'sheet' in resp.headers["Content-Type"]:
            with open(f'./data/indicative_margin.xlsx', 'wb') as stream:
                stream.write(resp.data)
            log.info(f"Results saved.")


def save_to_json(api_: CpmeApi, p: dict):
    fancy(p, 'QUERY_PARAMS:')
    resp = api.indicative_margin_get(**p, verbose=True)
    for item in resp:
        json_to_file(item['list_margins'], file_name='./data/indicative_margin' + str(item['business_date']))


if __name__ == '__main__':
    api = CpmeApi(configuration=config)
    bds = get_business_date(all_dates=True, api=api)

    params = {'business_date_from': bds[1],  # previous business date
              'business_date_to': bds[0],  # current business date
              'live': 'false'}

    save_to_json(api, params)

    params = {'clearing_house': 'EUXCDEFF',
              'products': ['FDAX', 'CONF'],
              'format': 'XLSX',
              'business_date': bds[0]}  # current business date

    config.return_json = False
    save_to_excel(api, params)
    api.close()
