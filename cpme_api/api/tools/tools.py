from typing import Union, List
import random
import logging
from itertools import groupby
from cpme_api.api import CpmeApi, Configuration


log = logging.getLogger('cpme_api')


def get_business_date(prev=False, all_dates=False, api: CpmeApi = None) -> Union[int, List[int]]:
    """Return current business date as default"""
    assert isinstance(prev, bool), "prev must be bool"
    assert isinstance(all_dates, bool), "all must be bool"
    if not api:
        api = CpmeApi()
    log.debug(f'ENV<{api.configuration.env}> waiting for response... timeout={api.configuration.request_timeout}')
    response = api.snapshots_get(verbose=True)
    if hasattr(response, 'json'):
        res = response.json()['snapshots']
    else:
        res = response['snapshots']
    bd_list = [k for k, _ in groupby((x["business_date"] for x in res))]
    if all_dates:
        return bd_list
    if prev:
        return bd_list[-2]
    else:
        return bd_list[-1]


def get_series(prod_ids: List[str] = tuple(),
               date: int = None,
               max_len: int = None,
               max_tte: int = 0,
               futures_only=False,
               options_only=False,
               flex=False,
               api: CpmeApi = None,
               verbose=True) -> List[dict]:
    """add filter_f = lambda x: x['days_to_expiration'] == 0)"""
    assert max_len is None or isinstance(max_len, int), "max_len must be int"
    assert (date is None) or isinstance(date, int), "date must be int"
    assert isinstance(max_tte, int), "max_tte must be int"
    assert isinstance(futures_only, bool), "futures_only must be bool"
    assert isinstance(options_only, bool), "options_only must be bool"
    assert isinstance(prod_ids, tuple), "prod_ids must be tuple"
    if not api:
        api = CpmeApi()
    if date:
        resp = api.series_get(business_date=date,
                              products=prod_ids,
                              extrafields=api.get_extrafields('series'),
                              flex=flex,
                              verbose=verbose)
    else:
        resp = api.series_get(products=prod_ids,
                              extrafields=api.get_extrafields('series'),
                              flex=flex,
                              verbose=verbose)
    if hasattr(resp, 'json'):
        series = resp.json().get('list_series', [])
    else:
        series = resp['list_series']
    if futures_only:
        series = [k for k in series if not k.get('call_put_flag')]
    if options_only:
        series = [k for k in series if k.get('call_put_flag')]
    if max_tte:
        return [k for k in series if k['days_to_expiration'] <= max_tte][:max_len]
    return series[:max_len]


def get_live_snapshot(date: int, ts_only=False, random_flag=False, api: CpmeApi = None) -> Union[dict, int]:
    """
    if ts_only=True and random_flag=True = return only one timestamp
    if ts_only=False and random_flag=True = return list of timestamps
    else:
        return live_snapshot records
    business_date,cash_available,live,live_timestamp,otc_available
    20220906,True,True,0,True
    20220906,True,True,1662423998525,True
    """
    assert isinstance(date, int), "date must be int"
    if not api:
        api = CpmeApi()
    res = api.live_snapshots_get(business_date=date, verbose=True)
    if hasattr(res, 'json'):
        res = res.json()
    if not res:
        return []
    index = random.randint(0, len(res['snapshots']) - 1)
    if ts_only:
        if random_flag:
            return res['snapshots'][index]['live_timestamp']
        else:
            return [x['live_timestamp'] for x in res['snapshots']]
    if random_flag:
        return res['snapshots'][index]
    else:
        return res['snapshots']
