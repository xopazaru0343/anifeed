"""
Anime domain model.

This module defines the core Anime data structure used throughout the application.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Anime:
    """
    Represents anime metadata retrieved from anime listing services.

    This is an immutable value object that stores core anime information.
    Uses frozen dataclass to ensure thread-safety and hashability.

    Attributes:
        title_romaji: The romanized Japanese title (e.g., "Shingeki no Kyojin")
        title_english: The official English title (e.g., "Attack on Titan")
        status: Current airing status (e.g., "RELEASING", "FINISHED", "NOT_YET_RELEASED")
        episodes: Total number of episodes. None if unknown or still airing

    Example:
        >>> anime = Anime(
        ...     title_romaji="Kimetsu no Yaiba",
        ...     title_english="Demon Slayer",
        ...     status="FINISHED",
        ...     episodes=26
        ... )
    """
    title_romaji: str
    title_english: str
    status: str
    episodes: Optional[int] = None
