"""
Nyaa.si search parameter enumerations.

This module defines all valid values for Nyaa.si search query parameters.
"""
__all__ = ["NyaaCategory", "NyaaFilter", "NyaaColumnToOrder", "NyaaOrder"]
from enum import Enum


class NyaaCategory(Enum):
    """
    Nyaa.si torrent categories for anime content.

    Values correspond to Nyaa's internal category codes.

    Members:
        DEFAULT: All anime (category 1_0)
        ENGLISH_TRANSLATED: English subbed anime (1_2)
        NON_ENGLISH_TRANSLATED: Non-English subbed (1_3)
        RAW: Raw/untranslated (1_4)
    """
    DEFAULT = "1_0"
    ENGLISH_TRANSLATED = "1_2"
    NON_ENGLISH_TRANSLATED = "1_3"
    RAW = "1_4"


class NyaaFilter(Enum):
    """
    Filter options for Nyaa.si search results.

    Members:
        NO_FILTER: Show all results (value "0")
        NO_REMAKES: Exclude remakes/duplicates (value "1")
        TRUSTED_ONLY: Only trusted uploaders (value "2")
    """
    NO_FILTER = "0"
    NO_REMAKES = "1"
    TRUSTED_ONLY = "2"


class NyaaColumnToOrder(Enum):
    """
    Columns available for sorting Nyaa.si search results.

    Members:
        SEEDS: Sort by number of seeders
        SIZE: Sort by file size
        DOWNLOADS: Sort by total downloads
        LEECHERS: Sort by number of leechers
    """
    SEEDS = "seeders"
    SIZE = "size"
    DOWNLOADS = "download"
    LEECHERS = "leechers"


class NyaaOrder(Enum):
    """
    Sort order direction for Nyaa.si results.

    Members:
        ASCENDING: Lowest to highest (value "asc")
        DESCENDING: Highest to lowest (value "desc")
    """
    ASCENDING = "asc"
    DESCENDING = "desc"
