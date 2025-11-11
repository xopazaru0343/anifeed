from typing import Protocol, Sequence, List

from anifeed.models.anime_model import Anime
from anifeed.models.torrent_model import Torrent


class AnimeRepository(Protocol):
    """Persistence port for cached anime lists."""
    def save_batch(self, animes: Sequence[Anime]) -> None:
        ...

    def load(self) -> List[Anime]:  # For now just create a simple select with no filters
        ...




class TorrentRepository(Protocol):
    """Optional cache/history port for torrents."""
    def save_batch(self, torrents: Sequence[Torrent]) -> None:
        ...

    def load(self) -> List[Torrent]:  # For now just create a simple select with no filters
        ...
