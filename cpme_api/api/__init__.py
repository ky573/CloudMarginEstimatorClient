"""
Base namespace with Post, Get class definition
which keep all necessary properties, attributes, parameters
used for particular api endpoint
"""
from .endpoints import GET, POST, GET_ENDPOINTS, POST_ENDPOINTS
from .cpme_api import CpmeApi
from cpme_api.api.feature.utils import fancy
from cpme_api.api.configuration import Configuration


__all__ = ["GET",
           "POST",
           "GET_ENDPOINTS",
           "POST_ENDPOINTS",
           "fancy",
           "CpmeApi",
           "Configuration"]
