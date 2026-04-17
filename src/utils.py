"""
Utility functions and classes for Sandbox Project.

This module provides common utility functions that can be used across
the project for various operations and helper functionality.
"""

import os
import sys
from typing import Any, Dict, List, Optional, Union


def get_project_root() -> str:
    """
    Get the root directory of the project.
    
    Returns:
        str: Path to the project root directory.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(current_dir)


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Safely get a value from a dictionary with a default fallback.
    
    Args:
        data: The dictionary to retrieve the value from.
        key: The key to look for in the dictionary.
        default: The default value to return if key is not found.
        
    Returns:
        Any: The value associated with the key, or the default value.
    """
    return data.get(key, default)


def ensure_list(value: Union[List[Any], Any]) -> List[Any]:
    """
    Ensure that the input value is a list.
    
    Args:
        value: The value to convert to a list if it isn't already.
        
    Returns:
        List[Any]: The value as a list. If value was already a list,
                  returns it unchanged. Otherwise, returns [value].
    """
    if isinstance(value, list):
        return value
    return [value]


def is_empty(value: Any) -> bool:
    """
    Check if a value is empty (None, empty string, empty list, etc.).
    
    Args:
        value: The value to check for emptiness.
        
    Returns:
        bool: True if the value is considered empty, False otherwise.
    """
    if value is None:
        return True
    if isinstance(value, (str, list, dict, tuple, set)):
        return len(value) == 0
    return False


class ConfigManager:
    """
    Simple configuration manager for storing and retrieving settings.
    """
    
    def __init__(self):
        """Initialize the configuration manager with an empty config dictionary."""
        self._config: Dict[str, Any] = {}
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: The configuration key.
            value: The value to associate with the key.
        """
        self._config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: The configuration key to retrieve.
            default: The default value if key is not found.
            
        Returns:
            Any: The configuration value or the default.
        """
        return self._config.get(key, default)
    
    def has(self, key: str) -> bool:
        """
        Check if a configuration key exists.
        
        Args:
            key: The configuration key to check.
            
        Returns:
            bool: True if the key exists, False otherwise.
        """
        return key in self._config
    
    def clear(self) -> None:
        """Clear all configuration values."""
        self._config.clear()
