from dataclasses import dataclass
import logging

from anifeed.db.repositories.sqlite_torrent_repository import SQLiteTorrentRepository, TorrentRepository
from anifeed.db.repositories.sqlite_anime_repository import SQLiteAnimeRepository, AnimeRepository
from anifeed.db.database import get_connection, init_db
from anifeed.models.config_model import ApplicationConfig
from anifeed.services.anime_service import AnimeService
from anifeed.services.torrent_service import TorrentService
from anifeed.services.similarity_service import SimilarityService
from anifeed.constants.anime_status_enum import AnimeStatus
from anifeed.constants.app_config import load_application_config
from anifeed.utils.log_utils import configure_root_logger, get_logger
from anifeed.utils.commons import UniversalPath
from anifeed.exceptions import AnifeedError


@dataclass
class Application:
    logger: logging.Logger
    anime_service: AnimeService
    torrent_service: TorrentService
    similarity_service: SimilarityService
    config: ApplicationConfig
    animerec: AnimeRepository
    torrentrec: TorrentRepository


def build_app() -> Application:
    configure_root_logger(level=logging.INFO)
    logger = get_logger(__name__)
    config = load_application_config()
    db_path = UniversalPath("database.db")
    init_db(db_path)
    return Application(
        logger=logger,
        anime_service=AnimeService(source=config.api),
        torrent_service=TorrentService(),
        similarity_service=SimilarityService(),
        config=config,
        animerec=SQLiteAnimeRepository(connection=get_connection(db_path=db_path)),
        torrentrec=SQLiteTorrentRepository(connection=get_connection(db_path=db_path))
    )


def main():
    try:
        app = build_app()
        animes = app.anime_service.get_user_anime_list(
            username=app.config.user,
            status=AnimeStatus.COMPLETED
        )

        if animes:
            app.animerec.save_batch(animes)
            app.animerec.load()
            for anime in animes:
                torrents = app.torrent_service.search(query=anime.title_romaji)
                app.torrentrec.save_batch(torrents=torrents, anime_id=anime.anime_id, anime_source=anime.source)
                break

    except AnifeedError as e:
        app.logger.error("Application error: %s", e)
        raise
    except ValueError as e:
        app.logger.error("Validation error: %s", e)
        raise
    except Exception as e:
        app.logger.exception("Unexpected error occurred: %s", e)
        raise


if __name__ == "__main__":
    main()
