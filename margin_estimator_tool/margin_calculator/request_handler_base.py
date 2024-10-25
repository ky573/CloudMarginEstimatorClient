"""
This module contains the RequestHandler class which is responsible for
sending requests to the API.
"""

from typing import Dict, Any
from abc import ABC, abstractmethod
from cpme_api.api import CpmeApi, Configuration
from cpme_api.models import set_data_validation, BodyEstimator


class RequestHandler(ABC):
    """Class to handle sending requests to the API."""
    def __init__(self):
        self.api: CpmeApi = self._setup_api()

    @abstractmethod
    def send_request(self, *args, **kwargs) -> Dict[str, Any]:
        """Abstract method for sending a request; to be implemented by subclasses."""
        pass

    def _setup_api(self) -> CpmeApi:
        """Sets up and returns the API for requests."""
        set_data_validation(False)
        config = Configuration()
        config.api_key = "9c40a29c-8b1d-4245-b3d9-2ffe5b5e9358"
        config.proxy = 'http://webproxy.deutsche-boerse.de:8080'
        config.enable_logging = True
        api = CpmeApi(configuration=config)
        return api
