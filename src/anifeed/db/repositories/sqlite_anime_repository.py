"""SQLite-backed implementation of the AnimeRepository protocol.

Provides persistent storage for Anime records using a shared SQLite connection.
All SQL operations use parameterized queries to prevent injection, and domain
conversion is delegated to mapper functions to keep this class focused purely
on persistence mechanics.
"""

import sqlite3
from typing import Sequence

from anifeed.db.mappers import anime_to_params, row_to_anime
from anifeed.db.repositories.interfaces import AnimeRepository
from anifeed.exceptions import AnifeedError
from anifeed.models.anime_model import Anime


UPSERT_SQL = """
INSERT OR REPLACE INTO anime
(anime_id, source, title_romaji, title_english, status, episodes)
VALUES (?, ?, ?, ?, ?, ?)
"""

SELECT_SQL = """
SELECT anime_id, source, title_romaji, title_english, status, episodes
FROM anime
ORDER BY title_romaji;
"""

DELETE_SQL = "DELETE FROM anime WHERE anime_id = ?;"


class SQLiteAnimeRepository(AnimeRepository):
    """Persist Anime records using a shared SQLite connection."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """
        Initialize repository with a configured SQLite connection.

        Args:
            connection: SQLite connection with row_factory and pragmas configured
        """
        self._connection = connection

    def save_batch(self, animes: Sequence[Anime]) -> None:
        """
        Upsert a batch of Anime records.

        Args:
            animes: Sequence of Anime instances to persist

        Raises:
            AnifeedError: If database operation fails
        """
        if not animes:
            return
        params = [anime_to_params(item) for item in animes]
        try:
            with self._connection:
                self._connection.executemany(UPSERT_SQL, params)
        except sqlite3.Error as exc:
            raise AnifeedError(f"Failed to save anime batch: {exc}") from exc

    def load(self) -> list[Anime]:
        """
        Retrieve all cached Anime entries.

        Returns:
            List of Anime instances sorted by romaji title

        Raises:
            AnifeedError: If database operation fails
        """
        try:
            cursor = self._connection.execute(SELECT_SQL)
            return [row_to_anime(row) for row in cursor.fetchall()]
        except sqlite3.Error as exc:
            raise AnifeedError(f"Failed to load anime records: {exc}") from exc
