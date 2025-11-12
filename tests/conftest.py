import pytest
from unittest.mock import Mock

from anifeed.models.anime_model import Anime
from anifeed.models.torrent_model import Torrent
from anifeed.models.config_model import ApplicationConfig, NyaaConfig


@pytest.fixture
def sample_anime():
    return Anime(
        anime_id=1,
        source="TestSource",
        title_romaji="Yofukashi no Utas",
        title_english="Call of the Night",
        status="RELEASING",
        episodes=25,
    )


@pytest.fixture
def sample_anime_list():
    return [
        Anime(
            anime_id=1,
            source="TestSource",
            title_romaji="Shingeki no Kyojin",
            title_english="Call of the Night",
            status="RELEASING",
            episodes=25,
        ),
        Anime(
            anime_id=2,
            source="TestSource",
            title_romaji="Kimetsu no Yaiba",
            title_english="Demon Slayer",
            status="FINISHED",
            episodes=26,
        ),
    ]


@pytest.fixture
def sample_torrent():
    return Torrent(
        torrent_id=1,
        title="[SubsPlease] Yofukashi no Uta - 01 [1080p].mkv",
        download_url="https://nyaa.si/download/1234567.torrent",
        size="1.3 GiB",
        seeders=150,
        leechers=25,
    )


@pytest.fixture
def sample_torrent_list():
    return [
        Torrent(
            torrent_id=1,
            title="[SubsPlease] Yofukashi no Uta - 01 [1080p].mkv",
            download_url="https://nyaa.si/download/1234567.torrent",
            size="1.3 GiB",
            seeders=150,
            leechers=25,
        ),
        Torrent(
            torrent_id=2,
            title="[Erai-raws] Yofukashi no Uta - 01 [720p].mkv",
            download_url="https://nyaa.si/download/1234568.torrent",
            size="800 MiB",
            seeders=80,
            leechers=10,
        ),
    ]


@pytest.fixture
def sample_config():
    nyaa_config = NyaaConfig(
        batch=["[batch]", "(batch)"],
        fansub=["[SubsPlease]", "[Erai-raws]"],
        resolution=["1080p", "720p"]
    )
    return ApplicationConfig(
        user="test_user",
        api="anilist",
        status=["WATCHING", "COMPLETED"],
        nyaa_config=nyaa_config
    )


@pytest.fixture
def anilist_api_response():
    """Sample AniList API response"""
    return {
        "data": {
            "MediaListCollection": {
                "lists": [{
                    "entries": [
                        {
                            "media": {
                                "title": {
                                    "romaji": "Yofukashi no Uta",
                                    "english": "Call of the Night"
                                },
                                "episodes": 13,
                                "status": "RELEASING"
                            }
                        }
                    ]
                }]
            }
        }
    }


@pytest.fixture
def mal_api_response():
    """Sample MAL API response"""
    return {
        "data": [
            {
                "node": {
                    "id": 16498,
                    "title": "Yofukashi no Uta",
                    "alternative_titles": {
                        "en": "Call of the Night"
                    },
                    "num_episodes": 13,
                    "status": "finished_airing"
                }
            }
        ]
    }


@pytest.fixture
def nyaa_html_response():
    """Sample Nyaa HTML response"""
    return """
    <html>
    <body>
        <table class="torrent-list">
            <tbody>
                <tr>
                    <td></td>
                    <td><a href="#">[SubsPlease] Yofukashi no Uta - 01 [1080p].mkv</a></td>
                    <td>
                        <a href="https://nyaa.si/download/1234567.torrent"></a>
                        <a href="magnet:?xt=urn:btih:abc123"></a>
                    </td>
                    <td>1.3 GiB</td>
                    <td></td>
                    <td>150</td>
                    <td>25</td>
                </tr>
            </tbody>
        </table>
    </body>
    </html>
    """


@pytest.fixture
def mock_anilist_api():
    mock = Mock()
    mock.get_user_anime_list.return_value = {
        "data": {"MediaListCollection": {"lists": [{"entries": []}]}}
    }
    return mock


@pytest.fixture
def mock_mal_api():
    mock = Mock()
    mock.get_user_anime_list.return_value = {"data": []}
    return mock


@pytest.fixture
def mock_nyaa_api():
    mock = Mock()
    mock.fetch_search_result.return_value = "<html><body></body></html>"
    return mock


@pytest.fixture
def mock_parser():
    mock = Mock()
    mock.parse_api_metadata.return_value = []
    return mock


@pytest.fixture
def mock_embedding_model():
    mock = Mock()
    mock.encode.return_value = [
        [1.0, 0.0, 0.0],
        [0.9, 0.1, 0.0],
        [0.7, 0.3, 0.0],
        [0.5, 0.5, 0.0],
        [0.1, 0.9, 0.0],
    ]
    return mock
