"""
Application configuration loader.

This module provides a factory function to load and parse the application
configuration from config.toml.
"""
from types import MappingProxyType

from anifeed.models.config_model import ApplicationConfig, NyaaConfig
from anifeed.utils.commons import TomlParser


def load_application_config() -> ApplicationConfig:
    """
    Load application configuration from config.toml file.

    Reads the TOML configuration file and constructs immutable configuration
    objects. Uses MappingProxyType to prevent accidental mutation of loaded data.

    Returns:
        ApplicationConfig: Fully populated and validated configuration object

    Raises:
        FileNotFoundError: If config.toml is not found
        tomllib.TOMLDecodeError: If config.toml is malformed

    Example:
        >>> config = load_application_config()
        >>> print(config.user)
        'myusername'
        >>> print(config.nyaa_config.resolution)
        ['1080p', '720p']
    """
    app_config = MappingProxyType(TomlParser.get_config("application"))
    nyaa_config = MappingProxyType(TomlParser.get_config("nyaa"))

    # Extract enabled statuses from config
    status_dict = app_config.get("status", {})
    enabled_statuses = [k for k, v in status_dict.items() if v]

    nyaa_config = NyaaConfig(
        batch=nyaa_config.get("batch"),
        fansub=nyaa_config.get("fansub"),
        resolution=nyaa_config.get("resolution")
    )

    return ApplicationConfig(
        user=app_config.get("user"),
        api=app_config.get("api"),
        status=enabled_statuses,
        nyaa_config=nyaa_config
    )
