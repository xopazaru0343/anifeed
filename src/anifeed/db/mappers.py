"""Bidirectional converters between SQLite rows and AniFeed domain models.

Mappers translate sqlite3.Row objects into immutable Anime/Torrent dataclasses
and convert domain objects into parameter tuples for prepared SQL statements.
This separation keeps repositories thin and ensures domain models remain
persistence-agnostic.
"""

from __future__ import annotations

from sqlite3 import Row
from urllib.parse import urljoin

from anifeed.constants import AnimeStatus
from anifeed.models.anime_model import Anime
from anifeed.models.torrent_model import Torrent


def row_to_anime(row: Row) -> Anime:
    """Create an Anime dataclass from a DB row."""
    return Anime(
        anime_id=row["anime_id"],
        source=row["source"],
        title_romaji=row["title_romaji"],
        title_english=row["title_english"],
        status=row['status'],
        episodes=row["episodes"],
    )


def anime_to_params(anime: Anime) -> tuple:
    """Convert an Anime instance into SQL parameter tuple."""
    return (
        anime.anime_id,
        anime.source,
        anime.title_romaji,
        anime.title_english,
        anime.status,
        anime.episodes,
    )


def row_to_torrent(row: Row) -> Torrent:
    """Create a Torrent dataclass from a DB row."""
    return Torrent(
        torrent_id=row["torrent_id"],
        title=row["title"].strip(),
        download_url=["download_url"],
        size=row["size"],
        seeders=row["seeders"],
        leechers=row["leechers"],
        anime_id=row["anime_id"],
        anime_source=row["anime_source"],
    )


def torrent_to_params(torrent: Torrent) -> tuple:
    """Convert a Torrent instance into SQL parameter tuple."""
    return (
        torrent.torrent_id,
        torrent.title,
        torrent.download_url,
        torrent.size,
        torrent.seeders,
        torrent.leechers,
        torrent.anime_id,
        torrent.anime_source,
    )
