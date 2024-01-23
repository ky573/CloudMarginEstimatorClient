#!/usr/bin/env python
"""
  Margin Calculation Request

  Request Body:
    'snapshot','clearing_currency','is_cross_margined','simulated_settlement_date','portfolio_components'
    *Required: portfolio_components

     *Portfolio Components: type, etd_portfolio, etd_csv, etd_cp005, otc_csv, otc_sensitivities, otc_cb202, otc_fpml, cash_json, cash_csv, repo_json, whatif_id

  Response Keys:
    'business_date','live','live_timestamp','clearing_currency','error','errors','portfolio_margin','rbm_margin','what_if_portfolio_margin','drilldowns','otc_drilldowns'

Example of post request with api.models objects.

You can import cpme_api.api.models as spec and refer to all available data model of resource body structure. e.g. estimator = spec.Estimator()

"""
from cpme_api.api import CpmeApi, Configuration, fancy
from cpme_api.api.feature.utils import json_to_file, csv_to_str
from cpme_api.api.tools import get_series, get_live_snapshot, get_business_date
import cpme_api.models as spec
from cpme_api.models import set_data_validation


def example_03(api: CpmeApi):
    """Dynamic composition of body request of estimator with many components"""
    # fetch some four option series 'GSK' or 'ODAX' with time to expiration <= 50
    product_ids = ('GSK', 'ODAX')
    series_list = get_series(prod_ids=product_ids, max_tte=50, options_only=True, api=api, max_len=4)

    # get random timestamp for current business data
    timestamp = get_live_snapshot(date=get_business_date(api=api), ts_only=True, random_flag=True, api=api)

    # define estimator body
    es_body = spec.BodyEstimator()
    # assign Live Snapshot
    es_body.snapshot = spec.Snapshot()
    es_body.snapshot.live = True
    es_body.snapshot.live_timestamp = timestamp
    es_body.clearing_currency = 'EUR'

    # Create first portfolio component for otc_csv
    otc_csv_comp = spec.BodyEstimatorPortfolioComponents()

    # upload data from csv file
    otc_csv_comp.otc_csv = spec.OtcCsv(csv=csv_to_str('./data/requests/otc_csv.csv'))

    # create second portfolio component for etd_portfolio
    etd_p_comp = spec.BodyEstimatorPortfolioComponents(type='etd_portfolio')
    inx = 0
    for series in series_list:
        inx += 1
        # create etd_portfolio positions
        pc_etd = spec.EtdPositionsInner()
        pc_etd.line_no = inx + 1
        pc_etd.iid = series['iid']
        pc_etd.product_id = series['product_id']
        pc_etd.net_ls_balance = 20 * inx
        etd_p_comp.etd_portfolio.append(pc_etd)

    # aggregate portfolio components
    es_body.portfolio_components.append(otc_csv_comp)
    es_body.portfolio_components.append(etd_p_comp)
    es_body.fancy(line_text='BODY:')

    # send request
    response = api.estimator_post(body=es_body.to_dict())

    # show and save result message
    fancy(response, 'RESP:')
    json_to_file(response, './data/estimator_etd_otc')


if __name__ == '__main__':
    set_data_validation(False)
    config = Configuration()
    config.api_key = "9c40a29c-8b1d-4245-b3d9-2ffe5b5e9358"
    config.proxy = 'http://webproxy.deutsche-boerse.de:8080'
    config.enable_logging = True
    api = CpmeApi(configuration=config)
    example_03(api)
    api.close()
