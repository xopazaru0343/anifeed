"""SQLite-backed implementation of the TorrentRepository protocol.

Manages persistent storage for Torrent metadata linked to Anime entries.
Uses a foreign key relationship (anime_id) to maintain referential integrity
and delegates row/domain conversion to mapper functions.
"""

from __future__ import annotations

import sqlite3
from typing import Sequence

from anifeed.db.mappers import row_to_torrent, torrent_to_params
from anifeed.db.repositories.interfaces import TorrentRepository
from anifeed.exceptions import AnifeedError
from anifeed.models.torrent_model import Torrent


INSERT_SQL = """
INSERT OR REPLACE INTO torrent
(torrent_id, title, download_url, size, seeders, leechers, anime_id, anime_source)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

SELECT_SQL = """
SELECT torrent_id, title, download_url, size, seeders, leechers, anime_id, anime_source
FROM torrent
ORDER BY seeders DESC;
"""


class SQLiteTorrentRepository(TorrentRepository):
    """Persist Torrent records mapped to Anime entries via SQLite."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """
        Initialize repository with a configured SQLite connection.

        Args:
            connection: SQLite connection with row_factory and pragmas configured
        """
        self._connection = connection

    def save_batch(self, torrents: Sequence[Torrent]) -> None:
        """
        Upsert a batch of Torrent records.

        Args:
            torrents: Sequence of Torrent instances to persist

        Raises:
            AnifeedError: If database operation fails
        """
        if not torrents:
            return
        params = [torrent_to_params(item) for item in torrents]
        try:
            with self._connection:
                self._connection.executemany(INSERT_SQL, params)
        except sqlite3.Error as exc:
            raise AnifeedError(f"Failed to save torrent batch: {exc}") from exc

    def load(self) -> list[Torrent]:
        """
        Retrieve all cached Torrent entries.

        Returns:
            List of Torrent instances sorted by seeder count (descending)

        Raises:
            AnifeedError: If database operation fails
        """
        try:
            cursor = self._connection.execute(SELECT_SQL)
            return [row_to_torrent(row) for row in cursor.fetchall()]
        except sqlite3.Error as exc:
            raise AnifeedError(f"Failed to load torrent records: {exc}") from exc
