#!/usr/bin/env python
"""
Execute the script from ./example folder due to a relative path used in file name.

Example of async requests of four snapshots
 1. /clearing_currencies
 2. /series
 3. /live_snapshots
 4. /products

Every request use async_req parameter which returns a thread.

async_call_for_threads() just save results with callback function json_to_file without any blocking.

"""
from cpme_api.api import CpmeApi, Configuration
from cpme_api.api.feature.utils import json_to_file
from cpme_api.api.tools import get_business_date


def async_call_for_threads(jobs, callback, logger=None):
    """
    Event loop which calls callback function if any of job is finished.

    It returns Tuple of results with job.id once all jobs are done.
    """
    ids_done = list()
    rets = list()
    while True:
        counter = 0
        for job in jobs:
            if job.ready():
                counter += 1
                if job.id not in ids_done:
                    if logger:
                        logger.info(f"Request:{job.id} done")
                    # call back function
                    ret = callback.__call__(job.get(), job.id)
                    rets.append((job.id, ret))
                ids_done.append(job.id)
        if len(jobs) == counter:
            break
    return rets


config = Configuration()
config.api_key = "9c40a29c-8b1d-4245-b3d9-2ffe5b5e9358"
config.proxy = 'http://webproxy.deutsche-boerse.de:8080'
config.enable_logging = True
log = config.get_loggger()

api = CpmeApi(configuration=config)
prev_date = get_business_date(prev=True, api=api)

workers = list()
workers.append(api.clearing_currencies_get(live=False, verbose=True, async_req=True))
workers.append(api.series_get(products=['ODAX', 'FDAX'], verbose=True, async_req=True))
workers.append(api.live_snapshots_get(async_req=True))
workers.append(api.products_get(business_date=prev_date, async_req=True))

async_call_for_threads(workers, json_to_file, logger=log)

api.close()
