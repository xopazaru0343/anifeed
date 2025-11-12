"""
Torrent search service.

This module provides anime torrent search functionality using Nyaa.si.
"""
from typing import List

from anifeed.models.torrent_model import Torrent
from anifeed.models.nyaa_search_model import NyaaParameters
from anifeed.services.apis.nyaa_api import NyaaApi
from anifeed.services.parsers.nyaa_parser import NyaaParser
from anifeed.utils.log_utils import get_logger


class TorrentService:
    """
    Service for searching anime torrents on Nyaa.si.

    Provides a high-level interface for searching torrents with automatic
    HTML parsing and result extraction.

    Attributes:
        _api: Nyaa API client for HTTP requests
        _parser: HTML parser for extracting torrent metadata
        logger: Logger for service operations

    Example:
        >>> service = TorrentService()
        >>> torrents = service.search("Attack on Titan")
        >>> best = torrents[0]  # Sorted by seeders by default
        >>> print(f"{best.title} - {best.seeders} seeders")
    """

    def __init__(self, session=None, logger=None):
        """
        Initialize torrent service with Nyaa API and parser.

        Args:
            session: Optional requests.Session for HTTP requests
            logger: Optional logger instance
        """
        self._api = NyaaApi(session=session, logger=logger)
        self._parser = NyaaParser(logger=logger)
        self.logger = logger or get_logger(f"anifeed.services.{self.__class__.__name__}")

    def search(self, query: str, **kwargs) -> List[Torrent]:
        """
        Search for anime torrents on Nyaa.si.

        Searches Nyaa with the provided query string and optional filters.
        Results are sorted by seeders in descending order by default.

        Args:
            query: Search query (anime title)
            **kwargs: Optional NyaaParameters fields (f, s, o, c)
                     See NyaaParameters for available options
             Returns:
            List of Torrent objects sorted by seeders (descending)

        Raises:
            ValueError: If query is empty or whitespace
            NetworkError: If Nyaa request fails
            ParsingError: If HTML response cannot be parsed

        Example:
            >>> service = TorrentService()
            >>> # Basic search
            >>> torrents = service.search("Demon Slayer")

            >>> # With filters
            >>> from anifeed.constants import NyaaFilter
            >>> torrents = service.search(
            ...     "Demon Slayer",
            ...     f=NyaaFilter.TRUSTED_ONLY.value
            ... )
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")

        params = NyaaParameters(q=query.strip(), **kwargs)
        self.logger.debug("Searching torrents: %s", query)
        raw_html = self._api.fetch_search_result(params=params)
        torrents = self._parser.parse_api_metadata(metadata=raw_html)
        self.logger.info("Found %d torrents for %s", len(torrents), query)
        return torrents
