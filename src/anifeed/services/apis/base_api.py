"""
Base API client with HTTP functionality.

This module provides the base class for all API clients, extending HttpClient
with API-specific logging.
"""

from __future__ import annotations

import requests
from typing import Optional

from anifeed.utils.http_client import HttpClient
from anifeed.utils.log_utils import get_logger


class BaseApi(HttpClient):
    """
    Base class for API clients with HTTP capabilities.

    Extends HttpClient with API-specific logging namespace. All concrete
    API implementations should inherit from this class.

    Attributes:
        base_url: Base URL for the API
        session: Configured requests Session
        logger: Namespaced logger for API operations

    Example:
        >>> class MyApi(BaseApi):
        ...     def __init__(self):
        ...         super().__init__(base_url="https://api.example.com")
        ...     def fetch_data(self):
        ...         return self.get("/data").json()
    """

    def __init__(self,
                 base_url: Optional[str] = None,
                 session: Optional[requests.Session] = None,
                 logger=None
                 ):
        """
        Initialize base API client.

        Args:
            base_url: Optional base URL for all API requests
            session: Optional custom requests.Session
            logger: Optional logger (defaults to namespaced logger)
        """
        super().__init__(base_url=base_url, session=session)
        self.logger = logger or get_logger(f"anifeed.services.apis.{self.__class__.__name__}")
