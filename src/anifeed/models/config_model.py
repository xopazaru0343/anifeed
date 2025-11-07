"""
Application configuration models.

This module defines immutable configuration data structures loaded from config.toml.
"""
from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class NyaaConfig:
    """
    Configuration for Nyaa torrent search filtering.

    Attributes:
        batch: List of batch release markers (e.g., ["[batch]", "(batch)"])
        fansub: Preferred fansub groups (e.g., ["[SubsPlease]", "[Erai-raws]"])
        resolution: Preferred video resolutions (e.g., ["1080p", "720p"])

    Example:
        >>> nyaa = NyaaConfig(
        ...     batch=["[batch]"],
        ...     fansub=["[SubsPlease]"],
        ...     resolution=["1080p"]
        ... )
    """
    batch: List[str]
    fansub: List[str]
    resolution: List[str]


@dataclass(frozen=True)
class ApplicationConfig:
    """
    Main application configuration loaded from config.toml.

    Attributes:
        user: Username for anime listing service (AniList or MAL)
        api: API source to use ("anilist" or "mal")
        status: List of enabled anime statuses to track (e.g., ["WATCHING", "COMPLETED"])
        nyaa_config: Nested configuration for torrent search preferences

    Example:
        >>> config = ApplicationConfig(
        ...     user="myusername",
        ...     api="anilist",
        ...     status=["WATCHING"],
        ...     nyaa_config=NyaaConfig(...)
        ... )
    """
    user: str
    api: str
    status: List[str]
    nyaa_config: NyaaConfig
