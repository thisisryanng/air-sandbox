"""
Test suite for the utils module.

This module contains comprehensive tests for all utility functions
and classes in the src.utils module.
"""

import pytest
import os
import tempfile
from datetime import datetime
from unittest.mock import patch, mock_open

from src.utils import (
    get_current_timestamp,
    ensure_directory_exists,
    safe_get_dict_value,
    is_valid_file_path,
    ConfigManager
)


class TestGetCurrentTimestamp:
    """Test cases for get_current_timestamp function."""
    
    def test_timestamp_format(self):
        """Test that timestamp follows ISO format."""
        timestamp = get_current_timestamp()
        # Should match format YYYY-MM-DDTHH:MM:SS
        try:
            datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            pytest.fail("Timestamp format is incorrect")
    
    def test_timestamp_is_string(self):
        """Test that timestamp returns a string."""
        timestamp = get_current_timestamp()
        assert isinstance(timestamp, str)
    
    def test_timestamp_length(self):
        """Test that timestamp has expected length."""
        timestamp = get_current_timestamp()
        assert len(timestamp) == 19  # YYYY-MM-DDTHH:MM:SS


class TestEnsureDirectoryExists:
    """Test cases for ensure_directory_exists function."""
    
    def test_create_new_directory(self):
        """Test creating a new directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = os.path.join(temp_dir, "new_directory")
            result = ensure_directory_exists(test_path)
            assert result is True
            assert os.path.exists(test_path)
            assert os.path.isdir(test_path)
    
    def test_existing_directory(self):
        """Test with existing directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = ensure_directory_exists(temp_dir)
            assert result is True
    
    def test_nested_directory_creation(self):
        """Test creating nested directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_path = os.path.join(temp_dir, "level1", "level2", "level3")
            result = ensure_directory_exists(nested_path)
            assert result is True
            assert os.path.exists(nested_path)
    
    @patch('os.makedirs')
    def test_permission_error(self, mock_makedirs):
        """Test handling of permission errors."""
        mock_makedirs.side_effect = PermissionError("Permission denied")
        result = ensure_directory_exists("/invalid/path")
        assert result is False


class TestSafeGetDictValue:
    """Test cases for safe_get_dict_value function."""
    
    def test_existing_key(self):
        """Test getting existing key value."""
        data = {"name": "test", "count": 42}
        result = safe_get_dict_value(data, "name")
        assert result == "test"
    
    def test_nonexistent_key_with_default(self):
        """Test getting nonexistent key with default value."""
        data = {"name": "test"}
        result = safe_get_dict_value(data, "missing", "default")
        assert result == "default"
    
    def test_nonexistent_key_without_default(self):
        """Test getting nonexistent key without default value."""
        data = {"name": "test"}
        result = safe_get_dict_value(data, "missing")
        assert result is None
    
    def test_empty_dict(self):
        """Test with empty dictionary."""
        data = {}
        result = safe_get_dict_value(data, "key", "default")
        assert result == "default"
    
    def test_none_values(self):
        """Test with None values in dictionary."""
        data = {"key": None}
        result = safe_get_dict_value(data, "key", "default")
        assert result is None


class TestIsValidFilePath:
    """Test cases for is_valid_file_path function."""
    
    def test_valid_file_path(self):
        """Test with a valid file path."""
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            result = is_valid_file_path(temp_path)
            assert result is True
        finally:
            os.unlink(temp_path)
    
    def test_invalid_file_path(self):
        """Test with an invalid file path."""
        result = is_valid_file_path("/nonexistent/file.txt")
        assert result is False
    
    def test_directory_path(self):
        """Test with a directory path (should return False)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = is_valid_file_path(temp_dir)
            assert result is False
    
    def test_empty_path(self):
        """Test with empty path."""
        result = is_valid_file_path("")
        assert result is False
    
    def test_none_path(self):
        """Test with None path."""
        result = is_valid_file_path(None)
        assert result is False


class TestConfigManager:
    """Test cases for ConfigManager class."""
    
    def test_init_empty(self):
        """Test initialization without config data."""
        manager = ConfigManager()
        assert manager.to_dict() == {}
    
    def test_init_with_data(self):
        """Test initialization with config data."""
        config_data = {"key1": "value1", "key2": 42}
        manager = ConfigManager(config_data)
        assert manager.to_dict() == config_data
    
    def test_get_existing_key(self):
        """Test getting existing configuration key."""
        config_data = {"key1": "value1"}
        manager = ConfigManager(config_data)
        assert manager.get("key1") == "value1"
    
    def test_get_nonexistent_key(self):
        """Test getting nonexistent key returns default."""
        manager = ConfigManager()
        assert manager.get("nonexistent") is None
        assert manager.get("nonexistent", "default") == "default"
    
    def test_set_value(self):
        """Test setting configuration value."""
        manager = ConfigManager()
        manager.set("new_key", "new_value")
        assert manager.get("new_key") == "new_value"
    
    def test_update_config(self):
        """Test updating configuration with new values."""
        manager = ConfigManager({"key1": "value1"})
        new_config = {"key2": "value2", "key3": 123}
        manager.update(new_config)
        
        expected = {"key1": "value1", "key2": "value2", "key3": 123}
        assert manager.to_dict() == expected
    
    def test_update_overwrites_existing(self):
        """Test that update overwrites existing keys."""
        manager = ConfigManager({"key1": "old_value"})
        manager.update({"key1": "new_value"})
        assert manager.get("key1") == "new_value"
    
    def test_to_dict_returns_copy(self):
        """Test that to_dict returns a copy, not reference."""
        manager = ConfigManager({"key1": "value1"})
        config_copy = manager.to_dict()
        config_copy["key2"] = "value2"
        
        # Original should not be modified
        assert manager.get("key2") is None
        assert "key2" not in manager.to_dict()
