"""
AniList GraphQL response parser.

This module parses AniList GraphQL responses into Anime domain objects.
"""
from typing import List, Dict, Any

from anifeed.services.parsers.base_parser import BaseParser
from anifeed.models.anime_model import Anime
from anifeed.utils.commons import DictWrangler


class AniListParser(BaseParser):
    """
    Parser for AniList GraphQL API responses.

    Extracts anime metadata from AniList's nested GraphQL response structure
    and converts it into Anime domain objects.

    Example:
        >>> parser = AniListParser()
        >>> response = {"data": {"MediaListCollection": {"lists": [...]}}}
        >>> anime_list = parser.parse_api_metadata(response)
    """

    def parse_api_metadata(self, metadata: Dict[Any, Any]) -> List[Anime]:
        """
        Parse AniList GraphQL response into Anime objects.

        Recursively extracts anime entries from the nested GraphQL structure
        and maps them to domain Anime objects.

        Args:
            metadata: Raw GraphQL response dictionary

        Returns:
            List of Anime objects extracted from the response

        Example:
            >>> parser = AniListParser()
            >>> data = {
            ...     "data": {
            ...         "MediaListCollection": {
            ...             "lists": [{
            ...                 "entries": [{
            ...                     "media": {
            ...                         "title": {"romaji": "...", "english": "..."},
            ...                         "episodes": 12,
            ...                         "status": "FINISHED"
            ...                     }
            ...                 }]
            ...             }]
            ...         }
            ...     }
            ... }
            >>> anime_list = parser.parse_api_metadata(data)
        """
        metadata = DictWrangler.find_value_recursively(
            data=metadata, target_key="entries")
        res = [
            Anime(
                anime_id=DictWrangler.find_value_recursively(x, "id"),
                source=AniListParser.__class__.__name__,
                title_romaji=DictWrangler.find_value_recursively(x, "romaji"),
                title_english=DictWrangler.find_value_recursively(x, "english"),
                episodes=DictWrangler.find_value_recursively(x, "episodes"),
                status=DictWrangler.find_value_recursively(x, "status"),
                )
            for x in metadata]

        return res
