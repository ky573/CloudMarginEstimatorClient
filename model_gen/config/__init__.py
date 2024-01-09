"""
prioritizes environment variables over files as the best recommendation to keep your settings.
"""
from .config import Environment, Settings, PROJECT_ROOT, log
import os

settings = Settings()


__all__ = [
    "Environment",
    "settings",
    "PROJECT_ROOT",
    "log"
]


def data_folder_fix(path: str):
    """Check if a folder variable name is relative
    path starts with . and add global SCENARIO_PATH_FOLDER."""
    if path.startswith('./'):
        path = os.path.join(settings.scenario_path_folder, path.lstrip("./"))
    return path

