import os
from typing import Dict, Optional
from enum import EnumType

from anifeed.services.apis.base_api import BaseApi
from anifeed.constants.anime_status_enum import AnimeStatus

MAL_STATUS_MAP = {
    AnimeStatus.WATCHING: "watching",
    AnimeStatus.PLANNING: "plan_to_watch",
    AnimeStatus.COMPLETED: "completed",
    AnimeStatus.DROPPED: "dropped",
    AnimeStatus.PAUSED: "on_hold",
    AnimeStatus.REPEATING: "watching",
}


class MalApi(BaseApi):
    def __init__(self,
                 session=None,
                 logger=None,
                 ):
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
        status = self._translate_status(internal_status=status)
        payload_dict = {
            "status": status,
            "fields": "id,title,alternative_titles,status,num_episodes",
            "limit": 1000,
            "nsfw": "true"
            }
        r = self.get(f"/users/{username}/animelist", params=payload_dict)
        r.raise_for_status()
        return r.json()

    def _translate_status(self, internal_status: AnimeStatus) -> Optional[str]:
        """Translates the internal MediaStatus to the MAL API string."""
        return MAL_STATUS_MAP.get(internal_status)
