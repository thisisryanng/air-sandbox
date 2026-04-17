"""
Utility functions and classes for the Sandbox Project.

This module contains common utility functions that can be used throughout
the project for various helper operations and shared functionality.
"""

import os
import sys
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import logging


def get_current_timestamp() -> str:
    """
    Get the current timestamp as a formatted string.
    
    Returns:
        str: Current timestamp in ISO format (YYYY-MM-DDTHH:MM:SS)
    
    Example:
        >>> timestamp = get_current_timestamp()
        >>> print(timestamp)
        2023-12-07T14:30:45
    """
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def ensure_directory_exists(path: str) -> bool:
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        path (str): The directory path to create
        
    Returns:
        bool: True if directory exists or was created successfully, False otherwise
        
    Example:
        >>> success = ensure_directory_exists("./data/output")
        >>> print(success)
        True
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except (OSError, PermissionError) as e:
        logging.error(f"Failed to create directory {path}: {e}")
        return False


def safe_get_dict_value(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Safely get a value from a dictionary with a default fallback.
    
    Args:
        data (Dict[str, Any]): The dictionary to query
        key (str): The key to look up
        default (Any, optional): Default value if key not found. Defaults to None.
        
    Returns:
        Any: The value associated with the key, or default if not found
        
    Example:
        >>> data = {"name": "test", "count": 42}
        >>> value = safe_get_dict_value(data, "name", "unknown")
        >>> print(value)
        test
    """
    return data.get(key, default)


def is_valid_file_path(file_path: str) -> bool:
    """
    Check if a given file path is valid and accessible.
    
    Args:
        file_path (str): The file path to validate
        
    Returns:
        bool: True if file exists and is accessible, False otherwise
        
    Example:
        >>> valid = is_valid_file_path("./README.md")
        >>> print(valid)
        True
    """
    try:
        return os.path.isfile(file_path) and os.access(file_path, os.R_OK)
    except (OSError, TypeError):
        return False


class ConfigManager:
    """
    A simple configuration manager for handling project settings.
    
    This class provides basic functionality for managing configuration
    data throughout the application lifecycle.
    """

    def __init__(self, config_data: Optional[Dict[str, Any]] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_data (Optional[Dict[str, Any]]): Initial configuration data
        """
        self._config = config_data or {}

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key (str): The configuration key
            default (Any): Default value if key not found
            
        Returns:
            Any: The configuration value or default
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key (str): The configuration key
            value (Any): The value to set
        """
        self._config[key] = value

    def update(self, new_config: Dict[str, Any]) -> None:
        """
        Update configuration with new values.
        
        Args:
            new_config (Dict[str, Any]): New configuration data to merge
        """
        self._config.update(new_config)

    def to_dict(self) -> Dict[str, Any]:
        """
        Return configuration as a dictionary.
        
        Returns:
            Dict[str, Any]: Copy of the current configuration
        """
        return self._config.copy()
