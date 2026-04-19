"""
Tests for the utils module.
"""

import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch, mock_open

from src.utils import (
    setup_logging,
    load_json_file,
    save_json_file,
    get_project_root,
    ensure_directory,
    file_exists,
    list_files,
    ConfigManager
)


class TestSetupLogging:
    """Test cases for setup_logging function."""
    
    def test_setup_logging_default(self):
        """Test setup_logging with default level."""
        logger = setup_logging()
        assert logger.name == "src.utils"
    
    def test_setup_logging_custom_level(self):
        """Test setup_logging with custom level."""
        logger = setup_logging("DEBUG")
        assert logger.name == "src.utils"


class TestJsonOperations:
    """Test cases for JSON file operations."""
    
    def test_load_json_file_success(self):
        """Test successful JSON file loading."""
        test_data = {"key": "value", "number": 42}
        
        with TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "test.json"
            json_file.write_text(json.dumps(test_data))
            
            result = load_json_file(json_file)
            assert result == test_data
    
    def test_load_json_file_not_found(self):
        """Test loading non-existent JSON file."""
        with pytest.raises(FileNotFoundError):
            load_json_file("non_existent.json")
    
    def test_load_json_file_invalid_json(self):
        """Test loading invalid JSON file."""
        with TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "invalid.json"
            json_file.write_text("invalid json content")
            
            with pytest.raises(json.JSONDecodeError):
                load_json_file(json_file)
    
    def test_save_json_file(self):
        """Test saving data to JSON file."""
        test_data = {"key": "value", "list": [1, 2, 3]}
        
        with TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "output.json"
            save_json_file(test_data, json_file)
            
            assert json_file.exists()
            loaded_data = json.loads(json_file.read_text())
            assert loaded_data == test_data
    
    def test_save_json_file_creates_directory(self):
        """Test that save_json_file creates parent directories."""
        test_data = {"test": True}
        
        with TemporaryDirectory() as temp_dir:
            nested_file = Path(temp_dir) / "nested" / "dir" / "test.json"
            save_json_file(test_data, nested_file)
            
            assert nested_file.exists()
            assert nested_file.parent.exists()


class TestFileOperations:
    """Test cases for file operations."""
    
    def test_get_project_root_with_readme(self):
        """Test get_project_root when README.md exists."""
        with TemporaryDirectory() as temp_dir:
            readme_file = Path(temp_dir) / "README.md"
            readme_file.touch()
            
            # Mock __file__ to be in a subdirectory
            with patch('src.utils.__file__', str(Path(temp_dir) / "src" / "utils.py")):
                root = get_project_root()
                # Should find the temp_dir as root due to README.md
                assert root.name == Path(temp_dir).name
    
    def test_ensure_directory(self):
        """Test ensure_directory creates directories."""
        with TemporaryDirectory() as temp_dir:
            new_dir = Path(temp_dir) / "new" / "nested" / "directory"
            result = ensure_directory(new_dir)
            
            assert new_dir.exists()
            assert new_dir.is_dir()
            assert result == new_dir
    
    def test_file_exists(self):
        """Test file_exists function."""
        with TemporaryDirectory() as temp_dir:
            existing_file = Path(temp_dir) / "exists.txt"
            existing_file.touch()
            
            assert file_exists(existing_file) is True
            assert file_exists(Path(temp_dir) / "not_exists.txt") is False
    
    def test_list_files(self):
        """Test list_files function."""
        with TemporaryDirectory() as temp_dir:
            # Create test files
            (Path(temp_dir) / "file1.txt").touch()
            (Path(temp_dir) / "file2.py").touch()
            (Path(temp_dir) / "file3.txt").touch()
            
            # Test listing all files
            all_files = list_files(temp_dir)
            assert len(all_files) == 3
            
            # Test listing with pattern
            txt_files = list_files(temp_dir, "*.txt")
            assert len(txt_files) == 2
            
            # Test non-existent directory
            empty_list = list_files("non_existent_dir")
            assert empty_list == []


class TestConfigManager:
    """Test cases for ConfigManager class."""
    
    def test_config_manager_init_no_file(self):
        """Test ConfigManager initialization without existing config file."""
        with TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            manager = ConfigManager(config_path)
            
            assert manager.to_dict() == {}
    
    def test_config_manager_init_with_file(self):
        """Test ConfigManager initialization with existing config file."""
        test_config = {"database": {"host": "localhost", "port": 5432}}
        
        with TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "config.json"
            config_path.write_text(json.dumps(test_config))
            
            manager = ConfigManager(config_path)
            assert manager.to_dict() == test_config
    
    def test_config_manager_get(self):
        """Test ConfigManager get method."""
        manager = ConfigManager()
        manager._config = {
            "database": {"host": "localhost", "port": 5432},
            "debug": True
        }
        
        assert manager.get("debug") is True
        assert manager.get("database.host") == "localhost"
        assert manager.get("database.port") == 5432
        assert manager.get("non_existent") is None
        assert manager.get("non_existent", "default") == "default"
    
    def test_config_manager_set(self):
        """Test ConfigManager set method."""
        manager = ConfigManager()
        
        manager.set("debug", True)
        manager.set("database.host", "localhost")
        manager.set("database.port", 5432)
        
        config = manager.to_dict()
        assert config["debug"] is True
        assert config["database"]["host"] == "localhost"
        assert config["database"]["port"] == 5432
    
    def test_config_manager_save_load(self):
        """Test ConfigManager save and load functionality."""
        test_config = {"test": "value", "nested": {"key": "data"}}
        
        with TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / "test_config.json"
            
            # Create and save config
            manager1 = ConfigManager(config_path)
            manager1.set("test", "value")
            manager1.set("nested.key", "data")
            manager1.save()
            
            # Load config in new manager
            manager2 = ConfigManager(config_path)
            assert manager2.get("test") == "value"
            assert manager2.get("nested.key") == "data"
