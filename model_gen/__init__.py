__version__ = '2.0.0'

from model_gen.config import settings

get_current_env = settings.current_env

__all__ = ["get_current_env"]
