"""
Tests for the utils module.
"""

import pytest
import os
import tempfile
import shutil
from src.utils import (
    get_version,
    hello_world,
    ensure_directory,
    safe_get_dict_value,
    is_valid_string
)


class TestGetVersion:
    """Test cases for get_version function."""
    
    def test_get_version_returns_string(self):
        """Test that get_version returns a string."""
        version = get_version()
        assert isinstance(version, str)
        assert len(version) > 0
    
    def test_get_version_format(self):
        """Test that version follows semantic versioning pattern."""
        version = get_version()
        assert version == "0.1.0"


class TestHelloWorld:
    """Test cases for hello_world function."""
    
    def test_hello_world_default(self):
        """Test hello_world with default name."""
        result = hello_world()
        assert result == "Hello, World!"
    
    def test_hello_world_with_name(self):
        """Test hello_world with custom name."""
        result = hello_world("Alice")
        assert result == "Hello, Alice!"
    
    def test_hello_world_with_none(self):
        """Test hello_world with None name."""
        result = hello_world(None)
        assert result == "Hello, World!"
    
    def test_hello_world_with_empty_string(self):
        """Test hello_world with empty string name."""
        result = hello_world("")
        assert result == "Hello, !"


class TestEnsureDirectory:
    """Test cases for ensure_directory function."""
    
    def test_ensure_directory_creates_new(self):
        """Test that ensure_directory creates a new directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = os.path.join(temp_dir, "new_directory")
            result = ensure_directory(test_path)
            assert result is True
            assert os.path.isdir(test_path)
    
    def test_ensure_directory_existing(self):
        """Test that ensure_directory works with existing directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = ensure_directory(temp_dir)
            assert result is True
            assert os.path.isdir(temp_dir)
    
    def test_ensure_directory_nested(self):
        """Test that ensure_directory creates nested directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_path = os.path.join(temp_dir, "level1", "level2", "level3")
            result = ensure_directory(nested_path)
            assert result is True
            assert os.path.isdir(nested_path)


class TestSafeGetDictValue:
    """Test cases for safe_get_dict_value function."""
    
    def test_safe_get_existing_key(self):
        """Test getting value for existing key."""
        data = {"name": "Alice", "age": 30}
        result = safe_get_dict_value(data, "name")
        assert result == "Alice"
    
    def test_safe_get_missing_key_with_default(self):
        """Test getting value for missing key with default."""
        data = {"name": "Alice"}
        result = safe_get_dict_value(data, "age", 25)
        assert result == 25
    
    def test_safe_get_missing_key_no_default(self):
        """Test getting value for missing key without default."""
        data = {"name": "Alice"}
        result = safe_get_dict_value(data, "age")
        assert result is None
    
    def test_safe_get_empty_dict(self):
        """Test getting value from empty dictionary."""
        data = {}
        result = safe_get_dict_value(data, "key", "default")
        assert result == "default"


class TestIsValidString:
    """Test cases for is_valid_string function."""
    
    def test_is_valid_string_valid(self):
        """Test with valid non-empty strings."""
        assert is_valid_string("hello") is True
        assert is_valid_string("world") is True
        assert is_valid_string("123") is True
    
    def test_is_valid_string_empty(self):
        """Test with empty string."""
        assert is_valid_string("") is False
    
    def test_is_valid_string_whitespace_only(self):
        """Test with whitespace-only string."""
        assert is_valid_string("   ") is False
        assert is_valid_string("\t\n") is False
    
    def test_is_valid_string_non_string(self):
        """Test with non-string types."""
        assert is_valid_string(123) is False
        assert is_valid_string(None) is False
        assert is_valid_string([]) is False
        assert is_valid_string({}) is False
    
    def test_is_valid_string_with_content_and_whitespace(self):
        """Test with strings containing content and whitespace."""
        assert is_valid_string("  hello  ") is True
        assert is_valid_string("\thello\n") is True
