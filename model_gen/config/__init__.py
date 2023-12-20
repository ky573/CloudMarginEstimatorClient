"""
prioritizes environment variables over files as the best recommendation to keep your settings.
"""
from .config import Environment, Settings, PROJECT_ROOT


settings = Settings()


__all__ = [
    "Environment",
    "settings",
    "PROJECT_ROOT"
]
