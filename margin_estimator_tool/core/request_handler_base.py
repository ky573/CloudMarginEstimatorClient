"""
This module contains the RequestHandler base class which is responsible for
sending requests to the API.
"""


import sys
import json
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from cpme_api.api import CpmeApi, Configuration
from cpme_api.models import set_data_validation
import click
import requests
from margin_estimator_tool.core.utils import is_business_day


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

    def _get_business_date(self, date: Optional[str], version: Optional[str]) -> int:
        """
        Get the correct business date.
        - If a date is provided, use it as is.
        - If the version is 'SOD', return the latest business day before today.
        - Otherwise, return today's date.
        """
        if date:
            return int(date)

        if version == "SOD":
            current_date = datetime.today()
            current_date -= timedelta(days=1)

            while not is_business_day(current_date):
                current_date -= timedelta(days=1)

            return int(current_date.strftime('%Y%m%d'))

        return int(datetime.today().strftime('%Y%m%d'))

    def _check_for_error_in_response(self, response) -> None:
        """
        Handles the response and checks for trace_id indicating errors despite a 200 status code.
        If trace_id is present, the full response is printed and the program exits.
        """
        if "trace_id" in response:
            click.echo("An error occurred in the request. Full response details:")
            click.echo(json.dumps(response, indent=4))
            sys.exit(1)

        click.echo("Request successful.")
