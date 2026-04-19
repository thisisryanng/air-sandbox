"""
Core utility functions and classes for the Sandbox Project.

This module provides common utility functions that can be used throughout
the project for various operations like data processing, file handling,
and general helper functions.
"""

import os
import sys
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import json
import logging


def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    Set up logging configuration for the project.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def load_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load and parse a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Parsed JSON data as dictionary
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(data: Dict[str, Any], file_path: Union[str, Path]) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save as JSON
        file_path: Path where to save the JSON file
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path object pointing to the project root
    """
    current = Path(__file__).parent
    while current.parent != current:
        if (current / 'README.md').exists() or (current / '.git').exists():
            return current
        current = current.parent
    return Path.cwd()


def ensure_directory(directory: Union[str, Path]) -> Path:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory: Directory path to ensure exists
        
    Returns:
        Path object of the created/existing directory
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def file_exists(file_path: Union[str, Path]) -> bool:
    """
    Check if a file exists.
    
    Args:
        file_path: Path to check
        
    Returns:
        True if file exists, False otherwise
    """
    return Path(file_path).exists()


def list_files(directory: Union[str, Path], pattern: str = "*") -> List[Path]:
    """
    List files in a directory matching a pattern.
    
    Args:
        directory: Directory to search in
        pattern: Glob pattern to match files (default: "*")
        
    Returns:
        List of Path objects for matching files
    """
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        return []
    
    return list(path.glob(pattern))


class ConfigManager:
    """
    Simple configuration management class.
    
    Provides methods to load, save, and manage configuration data.
    """
    
    def __init__(self, config_path: Union[str, Path] = "config.json"):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = Path(config_path)
        self._config: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load configuration from file if it exists."""
        if self.config_path.exists():
            try:
                self._config = load_json_file(self.config_path)
            except (FileNotFoundError, json.JSONDecodeError):
                self._config = {}
    
    def save(self) -> None:
        """Save current configuration to file."""
        save_json_file(self._config, self.config_path)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key (supports dot notation like 'section.key')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key (supports dot notation like 'section.key')
            value: Value to set
        """
        keys = key.split('.')
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get the entire configuration as a dictionary.
        
        Returns:
            Copy of the configuration dictionary
        """
        return self._config.copy()
