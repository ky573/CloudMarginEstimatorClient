"""Utility functions for the margin_calculator package."""


from typing import Dict, List, Union, Tuple


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
