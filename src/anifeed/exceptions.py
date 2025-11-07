"""
Domain-specific exceptions for better error handling and testability.

This module defines a hierarchy of exceptions specific to the anifeed domain,
enabling precise error handling and better separation of concerns.
"""


class AnifeedError(Exception):
    """
    Base exception for all anifeed-specific errors.

    All custom exceptions in this application inherit from this base class,
    making it easy to catch any application-specific error.

    Example:
        >>> try:
        ...     # some anifeed operation
        ... except AnifeedError as e:
        ...     logger.error(f"Application error: {e}")
    """
    pass


class ConfigurationError(AnifeedError):
    """
    Raised when configuration is invalid or missing.

    Indicates problems with config.toml loading, parsing, or validation.

    Example:
        >>> if not config.user:
        ...     raise ConfigurationError("User not configured in config.toml")
    """
    pass


class AnimeSourceError(AnifeedError):
    """
    Raised when an invalid anime source is specified.

    Occurs when trying to use an anime API source that is not registered
    in the factory.

    Example:
        >>> try:
        ...     service = AnimeService(source="invalid")
        ... except AnimeSourceError as e:
        ...     print(f"Unknown source: {e}")
    """
    pass


class TorrentSearchError(AnifeedError):
    """
    Raised when torrent search operations fail.

    Indicates failures during torrent site queries or search result processing.

    Example:
        >>> if not query.strip():
        ...     raise TorrentSearchError("Search query cannot be empty")
    """
    pass


class ParsingError(AnifeedError):
    """
    Raised when API response or HTML parsing fails.

    Occurs when response data is malformed or doesn't match expected structure.

    Example:
        >>> if not soup.find('tbody'):
        ...     raise ParsingError("Invalid HTML: missing tbody element")
    """
    pass


class NetworkError(AnifeedError):
    """
    Raised when HTTP requests fail or timeout.

    Wraps network-related failures like connection errors, timeouts,
    or unexpected HTTP status codes.

    Example:
        >>> try:
        ...     response = api.get_data()
        ... except requests.RequestException as e:
        ...     raise NetworkError(f"API request failed: {e}") from e
    """
    pass
