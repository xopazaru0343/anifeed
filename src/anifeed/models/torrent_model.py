"""
Torrent domain model.

This module defines the torrent metadata structure retrieved from torrent sites.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Torrent:
    """
    Represents torrent metadata from anime torrent aggregators.

    This is an immutable value object for torrent search results.
    Frozen to ensure thread-safety and prevent accidental modification.

    Attributes:
        title: Full torrent title including release group and quality
               (e.g., "[SubsPlease] Anime Name - 01 [1080p].mkv")
        download_url: Direct URL to the .torrent file
        size: Human-readable file size (e.g., "1.3 GiB", "800 MiB")
        seeders: Number of users currently sharing the complete file
        leechers: Number of users currently downloading

    Example:
        >>> torrent = Torrent(
        ...     title="[SubsPlease] Anime - 01 [1080p].mkv",
        ...     download_url="https://nyaa.si/download/123.torrent",
        ...     size="1.3 GiB",
        ...     seeders=150,
        ...     leechers=25
        ... )
    """
    torrent_id: str
    title: str
    download_url: str
    size: str
    seeders: int
    leechers: int
