"""Tests for file utility functions in utils module."""

import os
import tempfile
import pytest
from pathlib import Path
from src.utils import (
    read_file_lines,
    write_list_to_file,
    get_file_size,
    file_exists,
    create_directory_if_not_exists
)


class TestReadFileLines:
    """Test cases for read_file_lines function."""

    def test_read_file_lines_basic(self):
        """Test reading lines from a file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write("line1\nline2\nline3\n")
            temp_file = f.name
        
        try:
            result = read_file_lines(temp_file)
            assert result == ["line1\n", "line2\n", "line3\n"]
        finally:
            os.unlink(temp_file)

    def test_read_file_lines_empty_file(self):
        """Test reading from an empty file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            temp_file = f.name
        
        try:
            result = read_file_lines(temp_file)
            assert result == []
        finally:
            os.unlink(temp_file)

    def test_read_file_lines_path_object(self):
        """Test reading lines using Path object."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write("test line\n")
            temp_file = f.name
        
        try:
            result = read_file_lines(Path(temp_file))
            assert result == ["test line\n"]
        finally:
            os.unlink(temp_file)

    def test_read_file_lines_nonexistent_file(self):
        """Test reading from a non-existent file."""
        with pytest.raises(FileNotFoundError):
            read_file_lines("nonexistent_file.txt")

    def test_read_file_lines_invalid_type(self):
        """Test reading with invalid file path type."""
        with pytest.raises(TypeError):
            read_file_lines(123)


class TestWriteListToFile:
    """Test cases for write_list_to_file function."""

    def test_write_list_to_file_basic(self):
        """Test writing list to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "test.txt")
            data = ["line1", "line2", "line3"]
            
            write_list_to_file(data, file_path)
            
            with open(file_path, 'r') as f:
                content = f.read()
            
            assert content == "line1\nline2\nline3\n"

    def test_write_list_to_file_empty_list(self):
        """Test writing empty list to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "empty.txt")
            
            write_list_to_file([], file_path)
            
            with open(file_path, 'r') as f:
                content = f.read()
            
            assert content == ""

    def test_write_list_to_file_path_object(self):
        """Test writing using Path object."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.txt"
            data = ["test"]
            
            write_list_to_file(data, file_path)
            
            with open(file_path, 'r') as f:
                content = f.read()
            
            assert content == "test\n"

    def test_write_list_to_file_overwrite_false_existing(self):
        """Test writing with overwrite=False when file exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "existing.txt")
            
            # Create existing file
            with open(file_path, 'w') as f:
                f.write("existing content")
            
            with pytest.raises(FileExistsError):
                write_list_to_file(["new data"], file_path, overwrite=False)

    def test_write_list_to_file_invalid_data_type(self):
        """Test writing with invalid data type."""
        with pytest.raises(TypeError):
            write_list_to_file("not a list", "test.txt")

    def test_write_list_to_file_invalid_data_contents(self):
        """Test writing with invalid data contents."""
        with pytest.raises(TypeError):
            write_list_to_file([1, 2, 3], "test.txt")

    def test_write_list_to_file_invalid_path_type(self):
        """Test writing with invalid path type."""
        with pytest.raises(TypeError):
            write_list_to_file(["data"], 123)


class TestGetFileSize:
    """Test cases for get_file_size function."""

    def test_get_file_size_basic(self):
        """Test getting file size."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("hello world")
            temp_file = f.name
        
        try:
            size = get_file_size(temp_file)
            assert size == 11  # "hello world" is 11 bytes
        finally:
            os.unlink(temp_file)

    def test_get_file_size_empty_file(self):
        """Test getting size of empty file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name
        
        try:
            size = get_file_size(temp_file)
            assert size == 0
        finally:
            os.unlink(temp_file)

    def test_get_file_size_path_object(self):
        """Test getting file size using Path object."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test")
            temp_file = f.name
        
        try:
            size = get_file_size(Path(temp_file))
            assert size == 4
        finally:
            os.unlink(temp_file)

    def test_get_file_size_nonexistent_file(self):
        """Test getting size of non-existent file."""
        with pytest.raises(FileNotFoundError):
            get_file_size("nonexistent_file.txt")

    def test_get_file_size_invalid_type(self):
        """Test getting file size with invalid type."""
        with pytest.raises(TypeError):
            get_file_size(123)


class TestFileExists:
    """Test cases for file_exists function."""

    def test_file_exists_true(self):
        """Test file_exists with existing file."""
        with tempfile.NamedTemporaryFile() as f:
            assert file_exists(f.name) == True

    def test_file_exists_false(self):
        """Test file_exists with non-existent file."""
        assert file_exists("nonexistent_file.txt") == False

    def test_file_exists_path_object(self):
        """Test file_exists using Path object."""
        with tempfile.NamedTemporaryFile() as f:
            assert file_exists(Path(f.name)) == True

    def test_file_exists_directory(self):
        """Test file_exists with directory (should return False)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            assert file_exists(temp_dir) == False

    def test_file_exists_invalid_type(self):
        """Test file_exists with invalid type."""
        with pytest.raises(TypeError):
            file_exists(123)


class TestCreateDirectoryIfNotExists:
    """Test cases for create_directory_if_not_exists function."""

    def test_create_directory_if_not_exists_new(self):
        """Test creating a new directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_dir = os.path.join(temp_dir, "new_directory")
            
            create_directory_if_not_exists(new_dir)
            
            assert os.path.isdir(new_dir)

    def test_create_directory_if_not_exists_existing(self):
        """Test with existing directory (should not raise error)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Should not raise any error
            create_directory_if_not_exists(temp_dir)
            assert os.path.isdir(temp_dir)

    def test_create_directory_if_not_exists_nested(self):
        """Test creating nested directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nested_dir = os.path.join(temp_dir, "level1", "level2", "level3")
            
            create_directory_if_not_exists(nested_dir)
            
            assert os.path.isdir(nested_dir)

    def test_create_directory_if_not_exists_path_object(self):
        """Test creating directory using Path object."""
        with tempfile.TemporaryDirectory() as temp_dir:
            new_dir = Path(temp_dir) / "new_directory"
            
            create_directory_if_not_exists(new_dir)
            
            assert new_dir.exists() and new_dir.is_dir()

    def test_create_directory_if_not_exists_invalid_type(self):
        """Test creating directory with invalid type."""
        with pytest.raises(TypeError):
            create_directory_if_not_exists(123)
