"""
Nyaa.si torrent site API client.

This module provides an interface for searching torrents on Nyaa.si.
"""

from dataclasses import asdict

from anifeed.services.apis.base_api import BaseApi
from anifeed.models.nyaa_search_model import NyaaParameters


class NyaaApi(BaseApi):
    """
    Nyaa.si torrent search API client.

    Provides methods for querying the Nyaa.si torrent aggregator with
    customizable search parameters.

    Example:
        >>> api = NyaaApi()
        >>> params = NyaaParameters(q="Attack on Titan")
        >>> html = api.fetch_search_result(params)
        >>> # Returns raw HTML for parsing
    """

    def __init__(
                self,
                session=None,
                logger=None):
        """
        Initialize Nyaa API client.

        Args:
            session: Optional requests.Session for HTTP requests
            logger: Optional logger instance
        """
        super().__init__(
            base_url="https://nyaa.si",
            session=session,
            logger=logger)

    def fetch_search_result(
            self,
            params: NyaaParameters,
            ) -> str:
        """
        Search Nyaa.si with the specified parameters.

        Executes a GET request to Nyaa.si with the search parameters
        and returns the raw HTML response for parsing.

        Args:
            params: NyaaParameters object with search configuration

        Returns:
            Raw HTML response as string

        Raises:
            requests.HTTPError: If request fails

        Example:
            >>> api = NyaaApi()
            >>> from anifeed.constants.nyaa_search_enum import NyaaFilter
            >>> params = NyaaParameters(
            ...     q="Demon Slayer",
            ...     f=NyaaFilter.TRUSTED_ONLY.value
            ... )
            >>> html = api.fetch_search_result(params)
        """
        r = self.get(params=asdict(params))
        r.raise_for_status()
        return r.text
