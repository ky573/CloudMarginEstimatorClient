"""
This module contains the RequestHandler base class which is responsible for
sending requests to the API.
"""

import sys
import json
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import click
import requests
from cpme_api.api import CpmeApi, Configuration
from cpme_api.models import set_data_validation


class RequestHandler(ABC):
    """Class to handle sending requests to the API."""

    def __init__(self) -> None:
        """Initializes a RequestHandler instance."""
        self._api: CpmeApi = self._setup_api()

    @abstractmethod
    def process_and_provide_output(self) -> None:
        """Abstract method for sending a request and exporting data; implemented by subclasses."""

    @staticmethod
    def _handle_request_error(error: Exception) -> None:
        """Handles request-related errors by printing a message to the user."""
        if isinstance(error, requests.exceptions.HTTPError):
            click.echo(f"HTTP Error: {error}", err=True)
        elif isinstance(error, requests.exceptions.RequestException):
            click.echo(f"Error sending request: {error}", err=True)
        else:
            click.echo(f"Error: {error}", err=True)

    @staticmethod
    def _setup_api() -> CpmeApi:
        """Sets up and returns the API for requests."""
        load_dotenv()
        set_data_validation(False)
        config = Configuration()
        config.api_key = os.getenv("API_KEY")
        config.proxy = os.getenv("PROXY")
        config.enable_logging = True
        api = CpmeApi(configuration=config)
        return api

    def _get_business_date(self, date: Optional[str], version: Optional[str]) -> int:
        """
        Get the correct business date.
        If a date is provided, use it as is.
        If the version is 'EOD', return the latest business day before today.
        Otherwise, return today's date.
        """
        if date:
            return int(date)

        if version == "EOD":
            current_date = datetime.today()
            current_date -= timedelta(days=1)

            while not self._is_business_day(current_date):
                current_date -= timedelta(days=1)

            return int(current_date.strftime("%Y%m%d"))

        return int(datetime.today().strftime("%Y%m%d"))

    @staticmethod
    def _check_for_error_in_response(response: Dict[str, Any]) -> None:
        """
        Handles the response and checks for trace_id indicating errors despite a 200 status code.
        If trace_id is present, the full response is printed and the program exits.
        Otherwise, user gets informed about successful request.
        """
        if "trace_id" in response:
            click.echo("An error occurred in the request. Full response details:")
            click.echo(json.dumps(response, indent=4))
            sys.exit(1)

        click.echo("Request successful.")

    @staticmethod
    def _is_business_day(current_date: datetime) -> bool:
        """Check if the current date is a weekend day."""
        return current_date.weekday() not in [5, 6]
