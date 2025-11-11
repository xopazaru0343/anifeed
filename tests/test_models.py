import pytest
from anifeed.models.anime_model import Anime
from anifeed.models.torrent_model import Torrent
from anifeed.models.config_model import NyaaConfig
from anifeed.models.nyaa_search_model import NyaaParameters
from anifeed.models.user_model import UserAnimeList
from anifeed.constants.nyaa_search_enum import NyaaFilter, NyaaCategory, NyaaOrder, NyaaColumnToOrder


class TestAnimeModel:
    def test_anime_creation(self):
        anime = Anime(
            anime_id=1,
            source="TestSource",
            title_romaji="Test Anime",
            title_english="Test Anime EN",
            status="RELEASING",
            episodes=12
        )
        assert anime.anime_id == 1
        assert anime.source == "TestSource"
        assert anime.title_romaji == "Test Anime"
        assert anime.title_english == "Test Anime EN"
        assert anime.status == "RELEASING"
        assert anime.episodes == 12

    def test_anime_optional_episodes(self):
        anime = Anime(
            anime_id=1,
            source="TestSource",
            title_romaji="Test Anime",
            title_english="Test Anime EN",
            status="RELEASING",
        )
        assert anime.episodes is None

    def test_anime_immutability(self):
        anime = Anime(
            anime_id=1,
            source="TestSource",
            title_romaji="Test Anime",
            title_english="Test Anime EN",
            status="RELEASING",
            episodes=12
        )
        with pytest.raises(AttributeError):
            anime.title_romaji = "New Title"

    def test_anime_equality(self):
        anime1 = Anime(1, "TestSource", "Title", "Title EN", "RELEASING", 12)
        anime2 = Anime(1, "TestSource", "Title", "Title EN", "RELEASING", 12)
        anime3 = Anime(2, "TestSource", "Other", "Other EN", "FINISHED", 24)

        assert anime1 == anime2
        assert anime1 != anime3


class TestTorrentModel:
    def test_torrent_creation(self):
        torrent = Torrent(
            torrent_id=1,
            title="Test Torrent",
            download_url="https://example.com/torrent",
            size="1.5 GiB",
            seeders=100,
            leechers=50
        )
        assert torrent.torrent_id == 1
        assert torrent.title == "Test Torrent"
        assert torrent.download_url == "https://example.com/torrent"
        assert torrent.size == "1.5 GiB"
        assert torrent.seeders == 100
        assert torrent.leechers == 50

    def test_torrent_immutability(self):
        torrent = Torrent(1, "Title", "url", "1GB", 10, 5)
        with pytest.raises(AttributeError):
            torrent.seeders = 20

    def test_torrent_equality(self):
        t1 = Torrent(1, "Title", "url", "1GB", 10, 5)
        t2 = Torrent(1, "Title", "url", "1GB", 10, 5)
        t3 = Torrent(2, "Other", "url2", "2GB", 20, 10)

        assert t1 == t2
        assert t1 != t3


class TestConfigModels:
    def test_nyaa_config_creation(self):
        config = NyaaConfig(
            batch=["[batch]"],
            fansub=["[SubsPlease]"],
            resolution=["1080p", "720p"]
        )
        assert config.batch == ["[batch]"]
        assert config.fansub == ["[SubsPlease]"]
        assert config.resolution == ["1080p", "720p"]

    def test_application_config_creation(self, sample_config):
        assert sample_config.user == "test_user"
        assert sample_config.api == "anilist"
        assert sample_config.status == ["WATCHING", "COMPLETED"]
        assert isinstance(sample_config.nyaa_config, NyaaConfig)

    def test_config_immutability(self, sample_config):
        with pytest.raises(AttributeError):
            sample_config.user = "new_user"


class TestNyaaSearchModel:
    def test_nyaa_parameters_defaults(self):
        params = NyaaParameters(q="test query")
        assert params.q == "test query"
        assert params.f == NyaaFilter.NO_FILTER.value
        assert params.s == NyaaColumnToOrder.SEEDS.value
        assert params.o == NyaaOrder.DESCENDING.value
        assert params.c == NyaaCategory.DEFAULT.value

    def test_nyaa_parameters_custom(self):
        params = NyaaParameters(
            q="anime",
            f=NyaaFilter.TRUSTED_ONLY.value,
            s=NyaaColumnToOrder.SIZE.value,
            o=NyaaOrder.ASCENDING.value,
            c=NyaaCategory.ENGLISH_TRANSLATED.value
        )
        assert params.q == "anime"
        assert params.f == NyaaFilter.TRUSTED_ONLY.value


class TestUserModel:
    def test_user_anime_list_creation(self, sample_anime_list):
        user_list = UserAnimeList(
            username="testuser",
            source="anilist",
            watching=sample_anime_list[:1],
            completed=sample_anime_list[1:],
            plan_to_watch=[]
        )
        assert user_list.username == "testuser"
        assert user_list.source == "anilist"
        assert len(user_list.watching) == 1
        assert len(user_list.completed) == 1

    def test_user_anime_list_optional_lists(self):
        user_list = UserAnimeList(
            username="test",
            source="mal"
        )
        assert user_list.watching is None
        assert user_list.completed is None
        assert user_list.plan_to_watch is None
