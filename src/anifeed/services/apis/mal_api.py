"""
MyAnimeList REST API client.

This module provides an interface to the MyAnimeList v2 REST API for fetching
user anime lists.
"""
import os
from typing import Dict, Optional
from enum import EnumType
import json
from anifeed.services.apis.base_api import BaseApi
from anifeed.constants import AnimeStatus

MAL_STATUS_MAP = {
    AnimeStatus.WATCHING: "watching",
    AnimeStatus.PLANNING: "plan_to_watch",
    AnimeStatus.COMPLETED: "completed",
    AnimeStatus.DROPPED: "dropped",
    AnimeStatus.PAUSED: "on_hold",
    AnimeStatus.REPEATING: "watching",
}


class MalApi(BaseApi):
    """
    MyAnimeList REST API client for anime data.

    Provides methods for querying user anime lists from MyAnimeList using their
    v2 REST API. Requires MAL_CLIENT_ID environment variable for authentication.

    Attributes:
        session: Configured with MAL authentication headers

    Example:
        >>> os.environ["MAL_CLIENT_ID"] = "your_client_id"
        >>> api = MalApi()
        >>> data = api.get_user_anime_list("username", AnimeStatus.WATCHING)
        >>> print(data["data"])
    """

    def __init__(self,
                 session=None,
                 logger=None,
                 ):
        """
        Initialize MAL API client with authentication.

        Args:
            session: Optional requests.Session for HTTP requests
            logger: Optional logger instance

        Note:
            Requires MAL_CLIENT_ID environment variable to be set.
        """
        super().__init__(
            base_url="https://api.myanimelist.net/v2",
            session=session, logger=logger
            )
        self.session.headers = {"X-MAL-CLIENT-ID": os.getenv("MAL_CLIENT_ID")}

    def get_user_anime_list(
            self,
            username: str,
            status: EnumType,
            ) -> Dict:
        """
        Fetch user's anime list from MAL filtered by status.

        Makes a REST API call to retrieve anime entries for the specified
        user and viewing status.

        Args:
            username: MyAnimeList username
            status: Internal AnimeStatus enum value

        Returns:
            Raw API response as dictionary

        Raises:
            requests.HTTPError: If API request fails

        Example:
            >>> api = MalApi()
            >>> response = api.get_user_anime_list("user123", AnimeStatus.WATCHING)
            >>> for item in response["data"]:
            ...     print(item["node"]["title"])
        """
        status = self._translate_status(internal_status=status)
        payload_dict = {
            "status": status,
            "fields": "id,title,alternative_titles,status,num_episodes",
            "limit": 1000,
            "nsfw": "true",
            "offset": 0
            }
        response = dict(data = list())
        has_paging=True
        while has_paging:
            size_animelist = len(response["data"])
            r = self.get(f"/users/{username}/animelist", params=payload_dict)
            r.raise_for_status()
            aux = r.json()
            response["data"].extend(aux["data"])
            if aux.get("paging").get("next"):
                payload_dict["offset"]+=payload_dict["limit"]
            else:
                has_paging=False
        
        return response

    def _translate_status(self, internal_status: AnimeStatus) -> Optional[str]:
        """
        Translate internal AnimeStatus to MAL status string.

        Args:
            internal_status: Internal AnimeStatus enum

        Returns:
            MAL API status string (e.g., "watching", "completed")

        Example:
            >>> api = MalApi()
            >>> api._translate_status(AnimeStatus.WATCHING)
            'watching'
        """
        return MAL_STATUS_MAP.get(internal_status)
