"""SQLite connection factory and idempotent migration runner.

This module centralizes database initialization, ensuring consistent connection
configuration (row factory, foreign keys, WAL journaling) and tracking applied
schema migrations to prevent re-execution on subsequent runs.
"""

from importlib import resources
from pathlib import Path
import sqlite3
from typing import Iterable

MIGRATIONS_PACKAGE = "anifeed.db.sql"


def get_connection(db_path: Path) -> sqlite3.Connection:
    """Create a configured SQLite connection (row factory, pragmas, WAL)."""
    connection = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    connection.execute("PRAGMA journal_mode = WAL;")
    connection.execute("PRAGMA busy_timeout = 5000;")
    return connection


def apply_migrations(connection: sqlite3.Connection, applied: Iterable[str]) -> None:
    """Run unapplied migration scripts in order and record them."""
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS schema_migrations (filename TEXT PRIMARY KEY)"
    )

    for name in sorted(resources.contents(MIGRATIONS_PACKAGE)):
        if not name.endswith(".sql") or name in applied:
            continue
        script = resources.read_text(MIGRATIONS_PACKAGE, name)
        cursor.executescript(script)
        cursor.execute(
            "INSERT INTO schema_migrations (filename) VALUES (?)",
            (name,),
        )

    connection.commit()


def init_db(db_path: Path) -> None:
    """Idempotent database initialisation entry point."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations (filename TEXT PRIMARY KEY)"
        )

        already_applied = {
            row["filename"]
            for row in cursor.execute("SELECT filename FROM schema_migrations")
        }
        apply_migrations(conn, already_applied)
