"""
Utility functions for the Sandbox Project.

This module contains common utility functions that can be used throughout
the project for various helper operations and basic functionality.
"""

import os
import sys
from typing import Any, Dict, List, Optional, Union


def get_version() -> str:
    """
    Get the current version of the project.
    
    Returns:
        str: The current version string.
    """
    return "0.1.0"


def hello_world(name: Optional[str] = None) -> str:
    """
    Generate a hello world greeting message.
    
    Args:
        name: Optional name to include in the greeting. If None, uses "World".
        
    Returns:
        str: A greeting message.
    """
    if name is None:
        name = "World"
    return f"Hello, {name}!"


def ensure_directory(path: str) -> bool:
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        path: The directory path to ensure exists.
        
    Returns:
        bool: True if directory exists or was created successfully, False otherwise.
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except (OSError, PermissionError):
        return False


def safe_get_dict_value(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Safely get a value from a dictionary with a default fallback.
    
    Args:
        data: The dictionary to get the value from.
        key: The key to look up.
        default: The default value to return if key is not found.
        
    Returns:
        Any: The value associated with the key, or the default value.
    """
    return data.get(key, default)


def is_valid_string(value: Any) -> bool:
    """
    Check if a value is a non-empty string.
    
    Args:
        value: The value to check.
        
    Returns:
        bool: True if value is a non-empty string, False otherwise.
    """
    return isinstance(value, str) and len(value.strip()) > 0
