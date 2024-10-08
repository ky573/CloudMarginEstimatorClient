"""
This module contains the RequestHandler class which is responsible for
sending requests to the API.
"""

from typing import Dict, Any
import requests
import click
from cpme_api.api import CpmeApi, Configuration
from cpme_api.api.feature.utils import csv_to_str
import cpme_api.models as spec
from cpme_api.models import set_data_validation, BodyEstimator


class RequestHandler:
    """Class to handle sending requests to the API."""
    def __init__(self):
        self.api: CpmeApi = self._setup_api()

    def post_request(self, business_date: int, portfolio: str) -> Dict[str, Any]:
        """Sends a POST request to the specified URL with the given headers and data."""
        request_body = self._setup_request_body(business_date, portfolio)

        try:
            response = self.api.estimator_post(body=request_body.to_dict())
            return response
        except requests.exceptions.HTTPError as e:
            click.echo(f"HTTP Error: {e}", err=True)
        except requests.exceptions.RequestException as e:
            click.echo(f"Error sending request: {e}", err=True)
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
        return {}

    def _setup_api(self) -> CpmeApi:
        """Sets up and returns the API for requests."""
        set_data_validation(False)
        config = Configuration()
        config.api_key = "9c40a29c-8b1d-4245-b3d9-2ffe5b5e9358"
        config.proxy = 'http://webproxy.deutsche-boerse.de:8080'
        config.enable_logging = True
        api = CpmeApi(configuration=config)
        return api

    def _setup_request_body(self, business_day: int, portfolio: str) -> BodyEstimator:
        request_body = spec.BodyEstimator()
        request_body.snapshot = spec.Snapshot()
        request_body.snapshot.live = True
        request_body.snapshot.business_date = business_day
        request_body.clearing_currency = 'EUR'

        etd_csv_comp = spec.BodyEstimatorPortfolioComponents()
        etd_csv_comp.etd_csv = spec.EtdCsv(csv=portfolio)

        request_body.portfolio_components.append(etd_csv_comp)

        return request_body
