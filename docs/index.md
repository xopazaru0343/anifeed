# AniFeed

Welcome to the AniFeed documentation!

## Overview

AniFeed is a Python application for tracking anime and searching for torrents from your anime list.

## Features

- Fetch anime lists from AniList or MyAnimeList
- Search for anime torrents on Nyaa.si
- Semantic similarity matching for finding relevant torrents
- Configurable torrent filters (resolution, fansub groups, etc.)

## Quick Start

```python
from anifeed.main import build_app
from anifeed.constants.anime_status_enum import AnimeStatus

# Initialize application
app = build_app()

# Fetch watching list
animes = app.anime_service.get_user_anime_list(
    username=app.config.user,
    status=AnimeStatus.WATCHING
)

# Search for torrents
torrents = app.torrent_service.search(animes[0].title_english)