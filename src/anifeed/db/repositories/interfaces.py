"""
Repository protocol definitions for anime and torrent persistence.

Defines the abstract interfaces that concrete repository implementations must
satisfy, enabling Dependency Inversion: services depend on these protocols
rather than SQLite-specific classes, making the persistence layer swappable.
"""

from typing import Protocol, Sequence

from anifeed.models.anime_model import Anime
from anifeed.models.torrent_model import Torrent


class AnimeRepository(Protocol):
    """Persistence port for cached anime lists."""

    def save_batch(self, animes: Sequence[Anime]) -> None:
        """Persist a batch of Anime records (insert or update)."""
        ...

    def load(self) -> list[Anime]:
        """Retrieve all cached Anime entries."""
        ...


class TorrentRepository(Protocol):
    """Optional cache/history port for torrents."""

    def save_batch(self, torrents: Sequence[Torrent]) -> None:
        """Persist a batch of Torrent records (insert or update)."""
        ...

    def load(self) -> Sequence[Torrent]:
        """Retrieve all cached Torrent entries."""
        ...
