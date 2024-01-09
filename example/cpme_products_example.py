#!/usr/bin/env python
"""
<products>: GET
  Description:
 Lists all exchange-traded products, Eurex and ECC. Only `product` and `instrument_type`
 are returned by default. Remaining attributes (see response) are returned
 only if specified in `extrafields`.

  Parameters:
    HEADER: {'x_dbp_apikey': 'X-DBP-APIKEY'}
    QUERY PARAMETERS: 'extrafields','business_date','live','live_timestamp'
    EXTRA_FIELDS:
      'product','instrument_type','clearing_house','prod_name','prod_isin',
      'underlying_isin','currency','product_type','extended_product_type',
      'margin_style_flag','exercise_style_flag','product_settlement_type',
      'final_settlement_time','product_tick_size','product_tick_value',
      'liquidation_group','xm_eligibility'
    *Required: 'x_dbp_apikey'

"""
import ipdb
from cpme_api.api import CpmeApi, fancy, Configuration, GET
from cpme_api.api.feature.utils import json_to_file


BD = '20220906'

API_KEY = 'b953e6e4-235e-4217-a7b0-ceb071a9dba1'

PARAM_PROD = {'business_date': BD,
              'live': 'false',
              'extrafields': ['underlying_isin', 'product_type'],
              'x_dbp_apikey': API_KEY,
              }


# @catch_exception(enable=False)
def example(api: CpmeApi):
    """global settings"""
    # ipdb.set_trace()
    # api.products_get(live='true', api_key=API_KEY)
    """parameter definition with validation"""
    # default_p = api.products_get()
    # ipdb.set_trace()
    # resp = api.products_get(**PARAM_PROD, timeout=5)
    resp = api.products_get(extrafields=api.get_extrafields(GET.products))
    # fancy(resp)
    json_to_file(resp, 'products')


if __name__ == '__main__':
    config = Configuration()
    config.api_key = API_KEY
    config.enable_logging = True
    config.enable_pooling = True
    config.return_json = True
    # config.debug = True
    # config.logger_file = 'debug_log5.log'

    api = CpmeApi(configuration=config)
    example(api)
    api.close()
