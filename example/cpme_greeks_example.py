#!/usr/bin/env python
"""
TODO add link to github README file
"""
from cpme_api.api import CpmeApi, Configuration
from cpme_api.api.feature.utils import json_to_file, load_csv_to_list
from cpme_api.api.tools import get_series
import cpme_api.models as spec


def example_instruments_from_file(api: CpmeApi):
    """
    load series from pre-stored csv file and get greeks value only for instruments of
    particular products
    """
    product_ids = ('D2TE', 'GSK')
    data_series = load_csv_to_list(folder='./example/data/snapshots', file_name='cli_20220906_0_0_series.csv')
    instruments_ids = list(map(lambda x: x['iid'], filter(lambda x: x['product_id'] in product_ids, data_series)))
    # create body
    greeks = spec.BodyGreeks()
    greeks.iids = instruments_ids[:10]
    greeks.greek_types = spec.GreekTypesInner.get_enum()
    greeks.fancy(line_text='BODY:')
    # send request
    response = api.greeks_post(body=greeks.to_dict())
    json_to_file(response, 'greeks')


def example_for_actual_instruments(api: CpmeApi):
    """
    Load filtered series for current business date
    """
    product_ids = ('D2TE', 'GSK')
    series = get_series(prod_ids=product_ids, max_tte=50, options_only=True, api=api)
    # create body
    greeks = spec.BodyGreeks()
    greeks.iids = list(map(lambda x: x['iid'], series))
    greeks.greek_types = spec.GreekTypesInner.get_enum()
    greeks.fancy(line_text='BODY:')
    # send request
    response = api.greeks_post(body=greeks.to_dict())
    json_to_file(response, 'greeks')


if __name__ == '__main__':
    config = Configuration()
    config.api_key = "9c40a29c-8b1d-4245-b3d9-2ffe5b5e9358"
    config.url = "https://api.developer.deutsche-boerse.com/prisma-margin-estimator-2-0-2-0-0"
    config.enable_logging = True
    config.enable_pooling = True
    config.return_json = True
    api = CpmeApi(configuration=config)
    # example_instruments_from_file(api)
    example_for_actual_instruments(api)
    api.close()
