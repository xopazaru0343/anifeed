"""
HTTP client with retry logic and session management.

This module provides a robust HTTP client with automatic retries,
connection pooling, and request logging.
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Any

from anifeed.utils import log_utils


class HttpClient:
    """
    Configurable HTTP client with retry logic and base URL support.

    Provides a simplified interface for making HTTP requests with automatic
    retries on failures, connection pooling, and request logging.

    Attributes:
        base_url: Optional base URL prepended to all relative paths
        session: Configured requests Session with retry logic
        logger: Logger instance for request/response logging
    Example:
        >>> client = HttpClient(base_url="https://api.example.com")
        >>> response = client.get("/users/123")
        >>> data = response.json()
    """

    def __init__(self,
                 base_url: Optional[str] = None,
                 session: Optional[requests.Session] = None,
                 logger=None
                 ):
        """
        Initialize HTTP client with optional base URL and session.
        Args:
            base_url: Optional base URL for all requests
            session: Optional custom requests.Session (creates default if None)
            logger: Optional logger instance (creates default if None)
        """
        self.base_url = base_url
        self.session = session or self._create_session()
        self.logger = logger or log_utils.get_logger(f"anifeed.utils.{self.__class__.__name__}")

    def _create_session(self) -> requests.Session:
        """
        Create a requests Session with retry configuration.
        Configures automatic retries for:
        - Network failures (max 3 attempts)
        - 500-level HTTP errors (Server errors)
        - Exponential backoff (0.3s base factor)
        Returns:
            Configured requests.Session instance
        """
        s = requests.Session()
        retries = Retry(total=3, backoff_factor=0.3, status_forcelist={500, 502, 503, 504})
        adapter = HTTPAdapter(max_retries=retries)
        s.mount("http://", adapter)
        s.mount("https://", adapter)
        return s

    def _build_url(self, path: Optional[str]) -> str:
        """
        Construct full URL from base URL and path.

        Args:
            path: Relative or absolute path

        Returns:
            Full URL string

        Example:
            >>> client = HttpClient(base_url="https://api.example.com")
            >>> client._build_url("/users")
            'https://api.example.com/users'
            >>> client._build_url("https://other.com/data")
            'https://other.com/data'
        """
        if not path:
            return self.base_url or ""
        if self.base_url and not path.startswith("http"):
            return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        return path

    def get(self, path: Optional[str] = None, **kwargs) -> requests.Response:
        """
        Perform HTTP GET request.

        Args:
            path: URL path (relative to base_url or absolute)
            **kwargs: Additional arguments passed to requests.get()
                     (params, headers, timeout, etc.)
             Returns:
            requests.Response object

        Example:
            >>> client = HttpClient(base_url="https://api.example.com")
            >>> response = client.get("/users", params={"page": 1})
            >>> response.raise_for_status()
        """
        url = self._build_url(path)
        self.logger.debug("HTTP GET %s %s", url, kwargs)
        return self.session.get(url, **kwargs)

    def post(self, path: Optional[str] = None, json: Any = None, data: Any = None, **kwargs) -> requests.Response:
        """
        Perform HTTP POST request.
        Args:
            path: URL path (relative to base_url or absolute)
            json: Optional JSON payload (auto-serialized and sets Content-Type)
            data: Optional form data or bytes
            **kwargs: Additional arguments passed to requests.post()

        Returns:
            requests.Response object

        Example:
            >>> client = HttpClient(base_url="https://api.example.com")
            >>> response = client.post("/users", json={"name": "John"})
            >>> response.raise_for_status()
        """
        url = self._build_url(path)
        self.logger.debug("HTTP POST %s json=%s data=%s kwargs=%s", url, json, data, kwargs)
        return self.session.post(url, json=json, data=data, **kwargs)
