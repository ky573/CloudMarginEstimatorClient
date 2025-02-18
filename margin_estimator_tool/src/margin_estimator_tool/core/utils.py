"""Utility functions for the margin_calculator package."""


from typing import Dict, List, Union, Tuple
from datetime import datetime, timedelta


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
                    items.extend(flatten_dict(sub_item, f"{new_key}_{idx + 1}", sep=sep).items())
            else:
                items.append((new_key, str(v)))
        else:
            items.append((new_key, v))
            
    return dict(items)
