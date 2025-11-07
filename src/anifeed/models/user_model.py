"""
User anime list model.

This module defines the structure for a user's complete anime collection.
"""
from dataclasses import dataclass
from typing import Optional, List, Literal

from anifeed.models.anime_model import Anime


@dataclass(frozen=True)
class UserAnimeList:
    """
    Represents a user's complete anime list organized by status.

    Aggregates a user's anime collection from AniList or MyAnimeList,
    categorized by viewing status.

    Attributes:
        username: The user's username on the anime listing service
        source: Which service the data comes from ("anilist" or "mal")
        watching: Currently watching anime. None if not fetched
        completed: Completed anime. None if not fetched
        plan_to_watch: Planned anime. None if not fetched

    Example:
        >>> user_list = UserAnimeList(
        ...     username="johndoe",
        ...     source="anilist",
        ...     watching=[anime1, anime2],
        ...     completed=[anime3, anime4]
        ... )
    """
    username: str
    source: Literal["anilist", "mal"]
    watching: Optional[List[Anime]] = None
    completed: Optional[List[Anime]] = None
    plan_to_watch: Optional[List[Anime]] = None
