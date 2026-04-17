"""
Tests for the utils module.
"""

import pytest
import os
from src.utils import (
    get_project_root,
    safe_get,
    ensure_list,
    is_empty,
    ConfigManager
)


class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_get_project_root(self):
        """Test that get_project_root returns a valid path."""
        root = get_project_root()
        assert isinstance(root, str)
        assert os.path.exists(root)
    
    def test_safe_get_existing_key(self):
        """Test safe_get with an existing key."""
        data = {"key1": "value1", "key2": 42}
        result = safe_get(data, "key1")
        assert result == "value1"
    
    def test_safe_get_missing_key_with_default(self):
        """Test safe_get with a missing key and default value."""
        data = {"key1": "value1"}
        result = safe_get(data, "missing_key", "default")
        assert result == "default"
    
    def test_safe_get_missing_key_no_default(self):
        """Test safe_get with a missing key and no default."""
        data = {"key1": "value1"}
        result = safe_get(data, "missing_key")
        assert result is None
    
    def test_ensure_list_with_list(self):
        """Test ensure_list with a list input."""
        input_list = [1, 2, 3]
        result = ensure_list(input_list)
        assert result == input_list
        assert result is input_list  # Should return the same object
    
    def test_ensure_list_with_single_value(self):
        """Test ensure_list with a single value."""
        result = ensure_list("single_value")
        assert result == ["single_value"]
    
    def test_ensure_list_with_none(self):
        """Test ensure_list with None."""
        result = ensure_list(None)
        assert result == [None]
    
    def test_is_empty_with_none(self):
        """Test is_empty with None."""
        assert is_empty(None) is True
    
    def test_is_empty_with_empty_string(self):
        """Test is_empty with empty string."""
        assert is_empty("") is True
    
    def test_is_empty_with_non_empty_string(self):
        """Test is_empty with non-empty string."""
        assert is_empty("hello") is False
    
    def test_is_empty_with_empty_list(self):
        """Test is_empty with empty list."""
        assert is_empty([]) is True
    
    def test_is_empty_with_non_empty_list(self):
        """Test is_empty with non-empty list."""
        assert is_empty([1, 2, 3]) is False
    
    def test_is_empty_with_empty_dict(self):
        """Test is_empty with empty dictionary."""
        assert is_empty({}) is True
    
    def test_is_empty_with_non_empty_dict(self):
        """Test is_empty with non-empty dictionary."""
        assert is_empty({"key": "value"}) is False
    
    def test_is_empty_with_zero(self):
        """Test is_empty with zero (should not be considered empty)."""
        assert is_empty(0) is False


class TestConfigManager:
    """Test ConfigManager class."""
    
    def test_config_manager_initialization(self):
        """Test ConfigManager initialization."""
        config = ConfigManager()
        assert isinstance(config._config, dict)
        assert len(config._config) == 0
    
    def test_config_manager_set_and_get(self):
        """Test setting and getting configuration values."""
        config = ConfigManager()
        config.set("test_key", "test_value")
        
        result = config.get("test_key")
        assert result == "test_value"
    
    def test_config_manager_get_with_default(self):
        """Test getting a non-existent key with default value."""
        config = ConfigManager()
        result = config.get("missing_key", "default_value")
        assert result == "default_value"
    
    def test_config_manager_get_missing_key_no_default(self):
        """Test getting a non-existent key without default value."""
        config = ConfigManager()
        result = config.get("missing_key")
        assert result is None
    
    def test_config_manager_has_existing_key(self):
        """Test checking for an existing key."""
        config = ConfigManager()
        config.set("existing_key", "value")
        
        assert config.has("existing_key") is True
    
    def test_config_manager_has_missing_key(self):
        """Test checking for a missing key."""
        config = ConfigManager()
        assert config.has("missing_key") is False
    
    def test_config_manager_clear(self):
        """Test clearing all configuration values."""
        config = ConfigManager()
        config.set("key1", "value1")
        config.set("key2", "value2")
        
        assert len(config._config) == 2
        
        config.clear()
        assert len(config._config) == 0
        assert config.has("key1") is False
        assert config.has("key2") is False
