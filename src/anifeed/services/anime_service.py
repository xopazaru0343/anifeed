"""
Anime listing service.

This module provides a unified interface for fetching user anime lists from
different anime tracking services (AniList, MyAnimeList).
"""
from typing import List, Literal

from anifeed.models.anime_model import Anime
from anifeed.constants.anime_status_enum import AnimeStatus
from anifeed.services.anime_service_factory import create_anime_api_service
from anifeed.utils.log_utils import get_logger


class AnimeService:
    """
    Service for fetching user anime lists from anime tracking platforms.

    Provides a consistent interface across different anime listing services
    (AniList, MyAnimeList) by delegating to source-specific API and parser
    implementations.

    Attributes:
        source: The anime listing service being used ("anilist" or "mal")
        logger: Logger for service operations
        _api: Source-specific API client
        _parser: Source-specific response parser

    Example:
        >>> service = AnimeService(source="anilist")
        >>> watching = service.get_user_anime_list("username", AnimeStatus.WATCHING)
        >>> for anime in watching:
        ...     print(anime.title_english)
    """

    def __init__(
            self,
            source: Literal["anilist", "mal"] = "anilist",
            session=None,
            logger=None
    ):
        """
        Initialize anime service for a specific source.

        Args:
            source: Anime listing service to use ("anilist" or "mal")
            session: Optional requests.Session for HTTP requests
            logger: Optional logger instance

        Raises:
            AnimeSourceError: If source is not recognized
        """
        self.source = source
        self.logger = logger or get_logger(f"anifeed.services.{self.__class__.__name__}")
        self._api, self._parser = create_anime_api_service(
            source=source,
            session=session,
            logger=logger
        )

    def get_user_anime_list(self, username: str, status: AnimeStatus) -> List[Anime]:
        """
        Fetch a user's anime list filtered by viewing status.

        Retrieves anime entries from the configured source (AniList or MAL)
        for the specified user and status.

        Args:
            username: Username on the anime listing service
            status: Filter by viewing status (WATCHING, COMPLETED, etc.)

        Returns:
            List of Anime objects matching the status filter

        Raises:
            ValueError: If username is empty or whitespace
            NetworkError: If API request fails
            ParsingError: If response cannot be parsed

        Example:
            >>> service = AnimeService(source="anilist")
            >>> watching = service.get_user_anime_list("john", AnimeStatus.WATCHING)
            >>> completed = service.get_user_anime_list("john", AnimeStatus.COMPLETED)
        """
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")

        self.logger.debug("Fetching anime for %s from %s", username, self.source)
        raw_data = self._api.get_user_anime_list(username=username, status=status)
        animes = self._parser.parse_api_metadata(metadata=raw_data)
        self.logger.info("Fetched %d anime entries", len(animes))
        return animes
