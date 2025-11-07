"""
Common utility classes for path handling, dictionary operations, and config parsing.

This module provides reusable utilities used throughout the application.
"""
__all__ = ["UniversalPath", "DictWrangler", "TomlParser"]

from pathlib import Path
from typing import Union, Dict
import tomllib
import os


class UniversalPath:
    """
    Cross-platform path resolver relative to the anifeed package root.

    Provides a unified way to construct absolute paths relative to the
    src/anifeed directory, regardless of the current working directory.

    Attributes:
        _path: The resolved absolute path as a string
    Example:
        >>> path = UniversalPath("config.toml")
        >>> print(path)
        '/absolute/path/to/anifeed/config.toml'
        >>> full_path = path / "subdir" / "file.txt"
    """

    def __init__(self, path_string: Union[str, 'Path']):
        """
        Initialize a path relative to the anifeed package root.
        Args:
            path_string: Relative path from src/anifeed/ directory
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._path = os.path.join(base_dir, str(path_string))

    def __str__(self) -> str:
        """Return the absolute path as a string."""
        return self._path

    def __repr__(self) -> str:
        """Return a representation showing the path."""
        return f'Path("{self._path}")'

    def __fspath__(self) -> str:
        """Support for os.fspath() protocol."""
        return self._path

    def __truediv__(self, other: Union[str, 'Path']) -> 'Path':
        """
        Join paths using the / operator.

        Args:
            other: Path component to append

        Returns:
            New UniversalPath with joined path

        Example:
            >>> base = UniversalPath("data")
            >>> full = base / "configs" / "app.toml"
        """
        other_path = str(other)
        retVal = os.path.join(self._path, other_path)
        return UniversalPath(retVal)


class DictWrangler:
    """
    Utility for navigating nested dictionary and list structures.

    Provides recursive search capabilities for finding values in deeply
    nested JSON-like data structures.
    """

    @classmethod
    def find_value_recursively(cls, data, target_key):
        """
        Recursively search for a key in nested dictionaries and lists.

        Performs depth-first search through nested data structures to find
        the first occurrence of a key.

        Args:
            data: The data structure to search (dict, list, or primitive)
            target_key: The key to search for

        Returns:
            The value associated with target_key, or None if not found

        Example:
            >>> data = {"a": {"b": {"c": "value"}}}
            >>> DictWrangler.find_value_recursively(data, "c")
            'value'

            >>> nested = {"items": [{"id": 1}, {"id": 2, "name": "test"}]}
            >>> DictWrangler.find_value_recursively(nested, "name")
            'test'
        """
        if isinstance(data, dict):
            if target_key in data:
                return data[target_key]

            for key, value in data.items():
                result = DictWrangler.find_value_recursively(value, target_key)
                if result is not None:
                    return result

        elif isinstance(data, list):
            for item in data:
                result = DictWrangler.find_value_recursively(item, target_key)
                if result is not None:
                    return result
        return None


class TomlParser:
    """
    TOML configuration file parser.

    Provides a simple interface for reading TOML configuration files
    from the anifeed package directory.
    """

    @classmethod
    def get_config(cls, table_name: str) -> Dict:
        """
        Load a specific table from config.toml.

        Args:
            table_name: Name of the top-level TOML table to retrieve
                       (e.g., "application", "nyaa")
               Returns:
            Dictionary containing the specified configuration table

        Raises:
            FileNotFoundError: If config.toml doesn't exist
            tomllib.TOMLDecodeError: If config.toml is malformed

        Example:
            >>> app_config = TomlParser.get_config("application")
            >>> print(app_config["user"])
            'myusername'
        """
        with open(file=UniversalPath("config.toml"), mode="rb") as f:
            retVal = tomllib.load(f).get(table_name)
        return retVal
