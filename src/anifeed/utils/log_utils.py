"""
Logging configuration and utilities.

This module provides centralized logging setup with console and optional
file output support.
"""
import logging
from typing import Optional
from logging.handlers import RotatingFileHandler


def configure_root_logger(level: int = logging.INFO, logfile: Optional[str] = None) -> logging.Logger:
    """
    Configure the root logger with console and optional file output.

    Sets up logging with a standardized format across all loggers. Includes
    optional rotating file handler for persistent logs.

    Args:
        level: Logging level (e.g., logging.INFO, logging.DEBUG)
        logfile: Optional path to log file. If provided, enables file logging
                with automatic rotation (10MB max, 3 backups)

    Returns:
        Configured root logger instance

    Example:
        >>> configure_root_logger(level=logging.DEBUG, logfile="app.log")
        >>> logger = logging.getLogger(__name__)
        >>> logger.info("Application started")
        2025-01-01 10:00:00 | INFO     | Application started
    """
    root = logging.getLogger()

    # Avoid reconfiguring if already set up
    if root.handlers:
        return root

    root.setLevel(level)
    format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s')

    # Console handler
    handler = logging.StreamHandler()
    handler.setFormatter(format)
    root.addHandler(handler)

    # Optional file handler with rotation
    if logfile:
        file_handler = RotatingFileHandler(
            logfile,
            maxBytes=10_000_000,  # 10 MB
            backupCount=3
        )
        file_handler.setFormatter(format)
        root.addHandler(file_handler)

    return root


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.

    Creates or retrieves a logger with the given name, enabling
    module-specific logging and filtering.

    Args:
        name: Logger name (typically __name__ or "package.module.Class")

    Returns:
        Logger instance

    Example:
        >>> logger = get_logger("anifeed.services.AnimeService")
        >>> logger.info("Service initialized")
        >>> logger.debug("Debug info with namespace")
    """
    return logging.getLogger(name)
