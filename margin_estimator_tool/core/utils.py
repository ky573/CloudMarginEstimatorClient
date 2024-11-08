"""Utility functions for the margin_calculator package."""

from typing import Dict, List, Union, Tuple, Optional
from datetime import datetime, timedelta
import os
import click


def is_business_day(current_date: datetime) -> bool:
    """Check if the current date is a weekend."""
    return current_date.weekday() not in [5, 6]


def collect_business_days(start_date: datetime, end_date: datetime) -> List[int]:
    """Collects all business days within the date range."""
    current_date = start_date
    business_days: List[int] = []

    while current_date <= end_date:
        if is_business_day(current_date):
            business_days.append(int(current_date.strftime("%Y%m%d")))
        current_date += timedelta(days=1)

    return business_days


def flatten_dict(
        d: Dict[str, Union[Dict, List, str]],
        parent_key: str = '',
        sep: str = '_'
) -> Dict[str, Union[Dict, List, str]]:
    """Flattens nested dictionaries and lists into a single-level dictionary."""
    items: List[Tuple[str, Union[Dict, List, str]]] = []
    for k, v in d.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            if len(v) > 0 and isinstance(v[0], dict):
                for idx, sub_item in enumerate(v):
                    items.extend(flatten_dict(sub_item, f'{new_key}_{idx + 1}', sep=sep).items())
            else:
                items.append((new_key, str(v)))
        else:
            items.append((new_key, v))
    return dict(items)


def check_estimator_arguments(date_from: str, date_to: str, export_dir: str) -> None:
    """Checks if the click arguments are valid for estimator."""
    try:
        datetime.strptime(date_from, "%Y%m%d")
        datetime.strptime(date_to, "%Y%m%d")
    except ValueError as e:
        raise click.BadParameter("Date format must be YYYYMMDD.") from e

    if not os.path.exists(export_dir):
        raise click.BadParameter(f"Export directory '{export_dir}' not found.")


def check_products_arguments(date: Optional[str], export_dir: str) -> None:
    """Checks if the click arguments are valid for products."""
    try:
        if date:
            datetime.strptime(date, "%Y%m%d")
    except ValueError as e:
        raise click.BadParameter("Date format must be YYYYMMDD.") from e

    if not os.path.exists(export_dir):
        raise click.BadParameter(f"Export directory '{export_dir}' not found.")
