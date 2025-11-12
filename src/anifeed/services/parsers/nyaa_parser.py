"""
Nyaa.si HTML response parser.

This module parses Nyaa.si search result HTML into Torrent domain objects.
"""
import re
from typing import List

from bs4 import BeautifulSoup

from anifeed.services.parsers.base_parser import BaseParser
from anifeed.models.torrent_model import Torrent


class NyaaParser(BaseParser):
    """
    Parser for Nyaa.si HTML search results.

    Scrapes Nyaa.si search result pages and extracts torrent metadata
    into Torrent domain objects.

    Example:
        >>> parser = NyaaParser()
        >>> html = "<html>...</html>"  # Nyaa search results
        >>> torrents = parser.parse_api_metadata(html)
    """

    def parse_api_metadata(self, metadata: str) -> List[Torrent]:
        """
        Parse Nyaa.si HTML into Torrent objects.

        Scrapes the search results table from Nyaa HTML and extracts
        torrent information (title, download URL, size, seeders, leechers).

        Args:
            metadata: Raw HTML string from Nyaa.si search

        Returns:
            List of Torrent objects extracted from the HTML

        Raises:
            AttributeError: If HTML structure is unexpected (no tbody)

        Example:
            >>> parser = NyaaParser()
            >>> html = '''
            ... <table class="torrent-list">
            ...   <tbody>
            ...     <tr>
            ...       <td></td>
            ...       <td><a>[SubsPlease] Anime - 01 [1080p].mkv</a></td>
            ...       <td><a href="/download/123.torrent">⬇</a></td>
            ...       <td>1.3 GiB</td>
            ...       <td></td>
            ...       <td>150</td>
            ...       <td>25</td>
            ...     </tr>
            ...   </tbody>
            ... </table>
            ... '''
            >>> torrents = parser.parse_api_metadata(html)
            >>> print(torrents[0].seeders)
            150
        """
        soup = BeautifulSoup(metadata, 'html.parser')
        res = []
        for row in soup.find('tbody').find_all('tr'):
            content = row.find_all("td")
            url_link = [x["href"] for x in content[1].find_all("a")]
            download_links = [x["href"] for x in content[2].find_all("a")]
            res.append(
                Torrent(
                    torrent_id=re.search("/view/([0-9]+)", url_link[0]).group(1),
                    title=content[1].text.replace("\n", ""),
                    download_url=download_links[0],
                    size=content[3].text,
                    seeders=int(content[5].text),
                    leechers=int(content[6].text),
                ))
        return res
