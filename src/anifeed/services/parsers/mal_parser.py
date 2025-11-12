"""
MyAnimeList REST API response parser.

This module parses MAL REST API responses into Anime domain objects.
"""
from typing import List, Dict, Any

from anifeed.services.parsers.base_parser import BaseParser
from anifeed.models.anime_model import Anime
from anifeed.utils.commons import DictWrangler


class MalParser(BaseParser):
    """
    Parser for MyAnimeList REST API responses.

    Extracts anime metadata from MAL's REST API response structure and
    converts it into Anime domain objects.

    Example:
        >>> parser = MalParser()
        >>> response = {"data": [{"node": {...}}, ...]}
        >>> anime_list = parser.parse_api_metadata(response)
    """

    def parse_api_metadata(self, metadata: Dict[Any, Any]) -> List[Anime]:
        """
        Parse MAL REST API response into Anime objects.

        Extracts anime entries from the MAL response and maps them to
        domain Anime objects, handling MAL's specific field naming.

        Args:
            metadata: Raw REST API response dictionary

        Returns:
            List of Anime objects extracted from the response

        Example:
            >>> parser = MalParser()
            >>> data = {
            ...     "data": [{
            ...         "node": {
            ...             "title": "Anime Title",
            ...             "alternative_titles": {"en": "English Title"},
            ...             "num_episodes": 24,
            ...             "status": "finished_airing"
            ...         }
            ...     }]
            ... }
            >>> anime_list = parser.parse_api_metadata(data)
        """
        metadata = DictWrangler.find_value_recursively(
            data=metadata, target_key="data")
        res = [
            Anime(
                anime_id=DictWrangler.find_value_recursively(x, "id"),
                source=self.__class__.__name__,
                title_romaji=DictWrangler.find_value_recursively(x, "title"),
                title_english=DictWrangler.find_value_recursively(x, "en"),
                episodes=DictWrangler.find_value_recursively(x, "num_episodes"),
                status=DictWrangler.find_value_recursively(x, "status"),
                )
            for x in metadata]

        return res
