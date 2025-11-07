"""
AniList GraphQL API client.

This module provides an interface to the AniList GraphQL API for fetching
user anime lists.
"""
from typing import Dict, Optional
from enum import EnumType

from anifeed.constants.anime_status_enum import AnimeStatus
from anifeed.services.apis.base_api import BaseApi
from anifeed.utils.commons import UniversalPath

ANILIST_STATUS_MAP = {
    AnimeStatus.WATCHING: "CURRENT",
    AnimeStatus.PLANNING: "PLANNING",
    AnimeStatus.COMPLETED: "COMPLETED",
    AnimeStatus.DROPPED: "DROPPED",
    AnimeStatus.PAUSED: "PAUSED",
    AnimeStatus.REPEATING: "REPEATING",
}


class AniListApi(BaseApi):
    """
    AniList GraphQL API client for anime data.

    Provides methods for querying user anime lists from AniList using their
    GraphQL API. Automatically translates internal status enums to AniList
    status strings.

    Attributes:
        _query_fetch_userlist: GraphQL query for fetching user lists

    Example:
        >>> api = AniListApi()
        >>> data = api.get_user_anime_list("username", AnimeStatus.WATCHING)
        >>> print(data["data"]["MediaListCollection"])
    """

    def __init__(self,
                 session=None,
                 query_path: Optional[str] = None,
                 logger=None
                 ):
        """
        Initialize AniList API client.

        Args:
            session: Optional requests.Session for HTTP requests
            query_path: Optional custom path to GraphQL query file
            logger: Optional logger instance
        """
        super().__init__(
            base_url="https://graphql.anilist.co",
            session=session,
            logger=logger)

        qpath = UniversalPath("services/apis/anilist_api/fetch_userlist.graphql")
        with open(qpath, mode="r", encoding="utf-8") as fh:
            self._query_fetch_userlist = fh.read()

    def get_user_anime_list(
            self,
            username: str,
            status: EnumType,
            ) -> Dict:
        """
        Fetch user's anime list from AniList filtered by status.

        Executes a GraphQL query to retrieve anime entries for the specified
        user and viewing status.

        Args:
            username: AniList username
            status: Internal AnimeStatus enum value

        Returns:
            Raw GraphQL response as dictionary

        Raises:
            requests.HTTPError: If API request fails

        Example:
            >>> api = AniListApi()
            >>> response = api.get_user_anime_list("user123", AnimeStatus.WATCHING)
            >>> entries = response["data"]["MediaListCollection"]["lists"][0]["entries"]
        """
        status = self._translate_status(internal_status=status)
        payload_dict = {
            "query": self._query_fetch_userlist,
            "variables": {"userName": username,
                          "status": status}
            }
        r = self.post(json=payload_dict)
        r.raise_for_status()
        return r.json()

    def _translate_status(self, internal_status: AnimeStatus) -> Optional[str]:
        """
        Translate internal AnimeStatus to AniList status string.

        Args:
            internal_status: Internal AnimeStatus enum

        Returns:
            AniList API status string (e.g., "CURRENT", "COMPLETED")

        Example:
            >>> api = AniListApi()
            >>> api._translate_status(AnimeStatus.WATCHING)
            'CURRENT'
        """
        return ANILIST_STATUS_MAP.get(internal_status)
