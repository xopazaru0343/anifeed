"""
Nyaa search parameters model.

This module defines the data structure for Nyaa.si search query parameters.
"""

from dataclasses import dataclass

from anifeed.constants.nyaa_search_enum import (
    NyaaCategory,
    NyaaColumnToOrder,
    NyaaFilter,
    NyaaOrder
)


@dataclass
class NyaaParameters:
    """
    Encapsulates search parameters for Nyaa.si torrent queries.

    Mutable dataclass that holds all query parameters with sensible defaults
    for anime torrent searches.

    Attributes:
        q: Search query string (anime title)
        f: Filter type (no filter, no remakes, or trusted only)
        s: Column to sort results by (seeders, size, downloads, or leechers)
        o: Sort order (ascending or descending)
        c: Category to search within (defaults to anime English-translated)

    Example:
        >>> params = NyaaParameters(
        ...     q="Demon Slayer",
        ...     f=NyaaFilter.TRUSTED_ONLY.value,
        ...     s=NyaaColumnToOrder.SEEDS.value
        ... )
    """
    q: str
    f: NyaaFilter = NyaaFilter.NO_FILTER.value
    s: NyaaColumnToOrder = NyaaColumnToOrder.SEEDS.value
    o: NyaaOrder = NyaaOrder.DESCENDING.value
    c: NyaaCategory = NyaaCategory.DEFAULT.value
