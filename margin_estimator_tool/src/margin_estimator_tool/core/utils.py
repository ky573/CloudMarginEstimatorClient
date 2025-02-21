"""Utility functions for the margin_calculator package."""


import csv
from typing import Dict, List, Union, Tuple, Any
from datetime import datetime, timedelta
from cpme_api.models import BodyEstimator
import cpme_api.models as spec


def is_business_day(current_date: datetime) -> bool:
    """
    Check if the current date is a weekend day.

    Args:
        current_date: date to be checked

    Returns:
        True if the day is not a weekend, false otherwise
    """
    return current_date.weekday() not in [5, 6]


def collect_business_days(start_date: datetime, end_date: datetime) -> List[int]:
    """
    Collects all business days within the date range.

    Args:
        start_date: starting date of the range
        end_date: ending date if the range

    Returns:
        A list of business days in desired range
    """
    current_date = start_date
    business_days: List[int] = []

    while current_date <= end_date:
        if is_business_day(current_date):
            business_days.append(int(current_date.strftime("%Y%m%d")))
        current_date += timedelta(days=1)

    return business_days


def flatten_dict(
        dictionary: Dict[str, Union[Dict, List, str]],
        parent_key: str = '',
        sep: str = '_'
        ) -> Dict[str, Union[Dict, List, str]]:
    """
    Flattens nested dictionaries and lists into a single-level dictionary.

    Args:
        dictionary: dictionary to be flattened
        parent_key: key from previous level
        sep: separator between levels

    Returns:
        Dictionary which was flattened into a single level, i.e. doesn't contain any
        other dictionaries
    """
    items: List[Tuple[str, Union[Dict, List, str]]] = []
    for k, v in dictionary.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            if len(v) > 0 and isinstance(v[0], dict):
                for idx, sub_item in enumerate(v):
                    items.extend(flatten_dict(sub_item, f"{new_key}_{idx + 1}", sep=sep).items())
            else:
                items.append((new_key, str(v)))
        else:
            items.append((new_key, v))
            
    return dict(items)


def setup_estimator_request_gui(business_day: int,
                                portfolio: str,
                                version: bool = True,
                                timestamp: int = 0
                                ) -> BodyEstimator:
    """
    Sets up the body for the POST request to /estimator endpoint.

    Args:
        business_day: required business date
        portfolio: portfolio to be sent to endpoint
        version: desired version
        timestamp: desired timestamp

    Returns:
        Estimator body to be used in request and sent to endpoint
    """
    request_body = setup_request_body(business_day, timestamp, version)

    etd_csv_comp = spec.BodyEstimatorPortfolioComponents()
    etd_csv_comp.etd_csv = spec.EtdCsv(csv=load_portfolio(portfolio))

    request_body.portfolio_components.append(etd_csv_comp)
    return request_body


def setup_estimator_request_inner(business_day: int,
                                  portfolio: str,
                                  version: bool = True,
                                  timestamp: int = 0
                                  ) -> BodyEstimator:
    """
    Sets up the body for the POST request to /estimator endpoint.

    Args:
        business_day: required business date
        portfolio: portfolio to be sent to endpoint
        version: desired version
        timestamp: desired timestamp

    Returns:
        Estimator body to be used in request and sent to endpoint
    """
    request_body = setup_request_body(business_day, timestamp, version)

    etd_p_comp = spec.BodyEstimatorPortfolioComponents(type='etd_portfolio')

    with open(portfolio, mode='r', newline='', encoding="utf-8") as file:
        reader = csv.reader(file)

        header = next(reader)

        for row in reader:
            pc_etd = spec.EtdPositionsInner()

            for key, value in zip(header, row):
                setattr(pc_etd, "_" + key, value)

            etd_p_comp.etd_portfolio.append(pc_etd)

    request_body.portfolio_components.append(etd_p_comp)
    return request_body

def setup_request_body(business_day: int, timestamp: int = 0, version: bool = True) -> BodyEstimator:
    """
    Sets up the body for the POST request to /estimator endpoint.

    Args:
        business_day: required business date
        version: desired version
        timestamp: desired timestamp

    Returns:
        Estimator body to be used in request and sent to endpoint
    """
    request_body = BodyEstimator()
    request_body.snapshot = spec.Snapshot()
    request_body.snapshot.live = version
    request_body.snapshot.business_date = business_day
    request_body.snapshot.live_timestamp = timestamp
    request_body.clearing_currency = "EUR"

    return request_body

def load_portfolio(portfolio: str) -> str:
    """Loads and returns the portfolio as a string."""
    with open(portfolio, 'r', encoding="utf-8") as f:
        return f.read()
