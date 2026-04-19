"""Tests for reverse_utils module."""

import pytest
from src.reverse_utils import reverse_string


def test_reverse_string_hello():
    """Test reversing 'hello' returns 'olleh'."""
    assert reverse_string('hello') == 'olleh'


def test_reverse_string_empty():
    """Test reversing empty string returns empty string."""
    assert reverse_string('') == ''


def test_reverse_string_single_char():
    """Test reversing single character string."""
    assert reverse_string('a') == 'a'


def test_reverse_string_palindrome():
    """Test reversing palindrome string."""
    assert reverse_string('racecar') == 'racecar'


def test_reverse_string_with_spaces():
    """Test reversing string with spaces."""
    assert reverse_string('hello world') == 'dlrow olleh'


def test_reverse_string_with_numbers():
    """Test reversing string with numbers."""
    assert reverse_string('123') == '321'


def test_reverse_string_with_special_chars():
    """Test reversing string with special characters."""
    assert reverse_string('!@#$') == '$#@!'
