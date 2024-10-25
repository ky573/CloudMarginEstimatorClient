from typing import Dict, Any
import requests
import click
from cpme_api.models import BodyEstimator
from .request_handler_base import RequestHandler
import cpme_api.models as spec


class EstimatorRequestHandler(RequestHandler):
    """Handler for sending requests to the /estimator endpoint."""

    def send_request(self, business_date: int, portfolio: str) -> Dict[str, Any]:
        """Sends a POST request to the /estimator endpoint with the specified data."""
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

    def _setup_request_body(self, business_day: int, portfolio: str) -> BodyEstimator:
        """Sets up the body for the POST request to /estimator endpoint."""
        request_body = BodyEstimator()
        request_body.snapshot = spec.Snapshot()
        request_body.snapshot.live = True
        request_body.clearing_currency = 'EUR'

        etd_csv_comp = spec.BodyEstimatorPortfolioComponents()
        etd_csv_comp.etd_csv = spec.EtdCsv(csv=portfolio)

        request_body.portfolio_components.append(etd_csv_comp)
        return request_body
