"""
Factory for creating anime API services.

This module implements the Factory pattern with a registry for extensibility,
allowing registration of new anime sources at runtime.
"""
from typing import Dict, Callable, Tuple
from anifeed.services.apis.base_api import BaseApi
from anifeed.services.parsers.base_parser import BaseParser
from anifeed.services.apis.anilist_api import AniListApi
from anifeed.services.apis.mal_api import MalApi
from anifeed.services.parsers.anilist_parser import AniListParser
from anifeed.services.parsers.mal_parser import MalParser
from anifeed.exceptions import AnimeSourceError


ApiParserFactory = Callable[[object, object], Tuple[BaseApi, BaseParser]]


_ANIME_SOURCE_REGISTRY: Dict[str, ApiParserFactory] = {
    "anilist": lambda session, logger: (
        AniListApi(session=session, logger=logger),
        AniListParser(logger=logger)
    ),
    "mal": lambda session, logger: (
        MalApi(session=session, logger=logger),
        MalParser(logger=logger)
    ),
}


def register_anime_source(name: str, factory: ApiParserFactory) -> None:
    """
    Register a new anime source (extension point).

    Allows runtime registration of custom anime sources without modifying
    the factory code, following the Open/Closed Principle.

    Args:
        name: Unique identifier for the source (case-insensitive)
        factory: Callable that takes (session, logger) and returns
                (BaseApi, BaseParser) tuple
    Example:
        >>> def kitsu_factory(session, logger):
        ...     return (KitsuApi(session, logger), KitsuParser(logger))
        >>> register_anime_source("kitsu", kitsu_factory)
        >>> api, parser = create_anime_api_service("kitsu")
    """
    _ANIME_SOURCE_REGISTRY[name.lower()] = factory


def create_anime_api_service(source: str, session=None, logger=None) -> Tuple[BaseApi, BaseParser]:
    """
    Create API client and parser for the specified anime source.

    Factory function that instantiates the appropriate API and parser
    based on the source name. Supports case-insensitive source names.

    Args:
        source: Anime listing service name ("anilist", "mal", or custom)
        session: Optional requests.Session for HTTP client
        logger: Optional logger instance

    Returns:
        Tuple of (API client, response parser) for the source

    Raises:
        AnimeSourceError: If source is not registered

    Example:
        >>> api, parser = create_anime_api_service("anilist")
        >>> raw_data = api.get_user_anime_list("user", AnimeStatus.WATCHING)
        >>> anime_list = parser.parse_api_metadata(raw_data)
    """
    factory = _ANIME_SOURCE_REGISTRY.get(source.lower())
    if factory is None:
        available = ", ".join(_ANIME_SOURCE_REGISTRY.keys())
        raise AnimeSourceError(
            f"Unknown anime source: '{source}'. Available: {available}"
        )
    return factory(session, logger)
