from .request_handler_base import RequestHandler
from typing import Dict, Any
from cpme_api.models import BodyEstimator
import cpme_api.models as spec


class EstimatorRequestHandler(RequestHandler):
    """Handler for sending requests to the /estimator endpoint."""

    def send_request(self, business_date: int, portfolio: str) -> Dict[str, Any]:
        """Sends a POST request to the /estimator endpoint with the specified data."""
        request_body = self._setup_request_body(business_date, portfolio)

        try:
            response = self.api.estimator_post(body=request_body.to_dict())
            return response
        except Exception as e:
            self._handle_request_error(e)
        return {}

    def _setup_request_body(self, business_day: int, portfolio: str) -> BodyEstimator:
        """Sets up the body for the POST request to /estimator endpoint."""
        request_body = BodyEstimator()
        request_body.snapshot = spec.Snapshot()
        request_body.snapshot.live = True
        request_body.snapshot.business_date = business_day
        request_body.clearing_currency = 'EUR'

        etd_csv_comp = spec.BodyEstimatorPortfolioComponents()
        etd_csv_comp.etd_csv = spec.EtdCsv(csv=portfolio)

        request_body.portfolio_components.append(etd_csv_comp)
        return request_body
