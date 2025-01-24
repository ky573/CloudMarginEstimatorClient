"""
This module contains logic for argument validation for CLI interface.
Implemented by Template Method design pattern.
"""

from datetime import datetime
from typing import Optional
import os
import click


class BaseArgumentValidator:
    """Base class for argument validation."""

    def validate_date(self, date: str) -> None:
        """Checks that date is in correct format."""
        try:
            datetime.strptime(date, "%Y%m%d")
        except ValueError as e:
            raise click.BadParameter("Date format must be YYYYMMDD.") from e

    def validate_export_dir(self, export_dir: str) -> None:
        """Checks that export directory exists."""
        if not os.path.exists(export_dir):
            raise click.BadParameter(f"Export directory '{export_dir}' not found.")

    def validate(self, **kwargs) -> None:
        """Override this method in subclasses to define specific validation logic."""
        raise NotImplementedError


class PostEstimatorValidator(BaseArgumentValidator):
    """Subclass to validate arguments for /estimator endpoint."""
    def validate(self, date_from: str, date_to: str, export_dir: str) -> None:
        """Implementation of validate method for /estimator endpoint."""
        self.validate_date(date_from)
        self.validate_date(date_to)
        self.validate_export_dir(export_dir)


class GetProductsValidator(BaseArgumentValidator):
    """Subclass to validate arguments for /products endpoint."""
    def validate(self, date: Optional[str], export_dir: Optional[str]) -> None:
        """Implementation of validate method for /products endpoint."""
        if date:
            self.validate_date(date)
        if export_dir:
            self.validate_export_dir(export_dir)


class GetSeriesValidator(BaseArgumentValidator):
    """Subclass to validate arguments for /series endpoint."""
    def validate(self, date: Optional[str], export_dir: Optional[str]) -> None:
        """Implementation of validate method for /series endpoint."""
        if date:
            self.validate_date(date)
        if export_dir:
            self.validate_export_dir(export_dir)


class GetLiveSnapshotsValidator(BaseArgumentValidator):
    """Subclass to validate arguments for /live_snapshots endpoint."""
    def validate(self, date: str) -> None:
        """Implementation of validate method for /live_snapshots endpoint."""
        self.validate_date(date)


class GetSnapshotsValidator(BaseArgumentValidator):
    """Subclass to validate arguments for /snapshots endpoint."""
    def validate(self, date_from: Optional[str], date_to: Optional[str]) -> None:
        """Implementation of validate method for /snapshots endpoint."""
        if date_from:
            self.validate_date(date_from)
        if date_to:
            self.validate_date(date_to)


class EtdPortfolioValidator(BaseArgumentValidator):
    """Subclass to validate arguments for /estimator endpoint for sending portfolio."""
    def validate(self, date: Optional[str], export_dir: Optional[str]) -> None:
        """Implementation of validate method for /estimator endpoint."""
        if date:
            self.validate_date(date)
        if export_dir:
            self.validate_export_dir(export_dir)
