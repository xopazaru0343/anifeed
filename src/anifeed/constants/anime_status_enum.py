"""
Anime viewing status enumeration.

This module defines the internal representation of anime viewing statuses,
independent of external API status strings.
"""
from enum import Enum, auto


class AnimeStatus(Enum):
    """
    Enumeration of anime viewing statuses.

    Provides a consistent internal representation that is mapped to
    API-specific status strings by the API adapters.

    Members:
        WATCHING: Currently watching
        PLANNING: Planning to watch
        COMPLETED: Finished watching
        DROPPED: Started but discontinued
        PAUSED: Temporarily paused
        REPEATING: Rewatching

    Example:
        >>> status = AnimeStatus.WATCHING
        >>> if status == AnimeStatus.WATCHING:
        ...     print("Currently airing")
    """
    WATCHING = auto()
    PLANNING = auto()
    COMPLETED = auto()
    DROPPED = auto()
    PAUSED = auto()
    REPEATING = auto()
