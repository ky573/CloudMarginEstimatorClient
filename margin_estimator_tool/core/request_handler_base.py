"""
This module contains the RequestHandler base class which is responsible for
sending requests to the API.
"""

from abc import ABC, abstractmethod
from cpme_api.api import CpmeApi, Configuration
from cpme_api.models import set_data_validation
import click
import requests


class RequestHandler(ABC):
    """Class to handle sending requests to the API."""
    def __init__(self):
        self.api: CpmeApi = self._setup_api()

    @abstractmethod
    def process_and_provide_output(self) -> None:
        """Abstract method for sending a request and exporting data; implemented by subclasses."""

    def _handle_request_error(self, error: Exception) -> None:
        """Handles request-related errors by printing a message to the user."""
        if isinstance(error, requests.exceptions.HTTPError):
            click.echo(f"HTTP Error: {error}", err=True)
        elif isinstance(error, requests.exceptions.RequestException):
            click.echo(f"Error sending request: {error}", err=True)
        else:
            click.echo(f"Error: {error}", err=True)

    def _setup_api(self) -> CpmeApi:
        """Sets up and returns the API for requests."""
        set_data_validation(False)
        config = Configuration()
        config.api_key = "9c40a29c-8b1d-4245-b3d9-2ffe5b5e9358"
        config.proxy = 'http://webproxy.deutsche-boerse.de:8080'
        config.enable_logging = True
        api = CpmeApi(configuration=config)
        return api
