"""
This module contains logic for argument validation for CLI.
Implemented by Template Method design pattern.
"""


from datetime import datetime
from typing import Optional
import os
import click


class BaseArgumentValidator:
    """Base class for argument validation."""

    @staticmethod
    def validate_date(date: str) -> None:
        """
        Checks that date is in correct format.

        Args:
            date: date to be validated
        """
        try:
            datetime.strptime(date, "%Y%m%d")
        except ValueError as e:
            raise click.BadParameter("Date format must be YYYYMMDD.") from e

    @staticmethod
    def validate_dir(directory: str) -> None:
        """
        Checks that directory exists.

        Args:
            directory: directory to be checked
        """
        if not os.path.exists(directory):
            raise click.BadParameter(f"Directory '{directory}' not found.")

    def validate(self, *args, **kwargs) -> None:
        """Override this method in subclasses to define specific validation logic."""
        raise NotImplementedError


class MarginCalculatorValidator(BaseArgumentValidator):
    """Subclass to validate arguments for /estimator endpoint."""
    def validate(self, csv_file: str, date_from: str, date_to: str, export_dir: str) -> None:
        """
        Implementation of validate method for /estimator endpoint.

        Args:
            csv_file: Csv file for portfolio
            date_from: starting date for the interval
            date_to: ending date for the interval
            export_dir: directory where data should be exported
        """
        self.validate_dir(csv_file)
        self.validate_date(date_from)
        self.validate_date(date_to)
        self.validate_dir(export_dir)


class GetProductsValidator(BaseArgumentValidator):
    """Subclass to validate arguments for /products endpoint."""
    def validate(self, date: Optional[str], export_dir: Optional[str]) -> None:
        """
        Implementation of validate method for /products endpoint.

        Args:
            date: date for the request
            export_dir: directory where data should be exported
        """
        if date:
            self.validate_date(date)
        if export_dir:
            self.validate_dir(export_dir)


class GetSeriesValidator(BaseArgumentValidator):
    """Subclass to validate arguments for /series endpoint."""
    def validate(self, date: Optional[str], export_dir: Optional[str]) -> None:
        """
        Implementation of validate method for /series endpoint.

        Args:
            date: date for the request
            export_dir: directory where data should be exported
        """
        if date:
            self.validate_date(date)
        if export_dir:
            self.validate_dir(export_dir)


class GetLiveSnapshotsValidator(BaseArgumentValidator):
    """Subclass to validate arguments for /live_snapshots endpoint."""
    def validate(self, date: str) -> None:
        """
        Implementation of validate method for /live_snapshots endpoint.

        Args:
            date: date for the request
        """
        self.validate_date(date)


class GetSnapshotsValidator(BaseArgumentValidator):
    """Subclass to validate arguments for /snapshots endpoint."""
    def validate(self, date_from: Optional[str], date_to: Optional[str]) -> None:
        """
        Implementation of validate method for /snapshots endpoint.

        Args:
            date_from: starting date for the interval
            date_to: ending date for the interval
        """
        if date_from:
            self.validate_date(date_from)
        if date_to:
            self.validate_date(date_to)


class EtdPortfolioValidator(BaseArgumentValidator):
    """Subclass to validate arguments for /estimator endpoint for sending portfolio."""
    def validate(self, csv_file: str, date: Optional[str], export_dir: Optional[str]) -> None:
        """
        Implementation of validate method for /estimator endpoint.

        Args:
            csv_file: portfolio file to be checked
            date: date for the request
            export_dir: directory where data should be exported
        """
        self.validate_dir(csv_file)
        if date:
            self.validate_date(date)
        if export_dir:
            self.validate_dir(export_dir)
