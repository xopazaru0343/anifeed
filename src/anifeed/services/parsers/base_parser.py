"""
Base parser for API responses.

This module provides the abstract base class for all API response parsers.
"""
from typing import Any

from anifeed.utils import log_utils


class BaseParser:
    """
    Abstract base class for API response parsers.

    Defines the interface that all concrete parsers must implement.
    Provides common logger initialization for all parsers.

    Attributes:
        logger: Namespaced logger for parser operations

    Example:
        >>> class MyParser(BaseParser):
        ...     def parse_api_metadata(self, metadata):
        ...         # Extract data from response
        ...         return parsed_data
    """

    def __init__(self, logger=None):
        """
        Initialize base parser with logger.

        Args:
            logger: Optional logger (defaults to namespaced logger)
        """
        self.logger = logger or log_utils.get_logger(f"anifeed.services.{self.__class__.__name__}")

    def parse_api_metadata(self, metadata: Any):
        """
        Parse API response metadata into domain models.

        Must be implemented by all subclasses to transform raw API
        responses into typed domain objects.

        Args:
            metadata: Raw API response (dict, str, etc.)

        Returns:
            Parsed domain objects (List[Anime], List[Torrent], etc.)

        Raises:
            NotImplementedError: If not overridden in subclass
        """
        raise NotImplementedError("parse_api_metadata must be implemented in subclasses")
