"""Tests for wordcount_utils module."""

import pytest
from src.wordcount_utils import count_words


class TestCountWords:
    """Test cases for the count_words function."""
    
    def test_basic_word_counting(self):
        """Test basic word counting functionality."""
        assert count_words('hello world') == 2
        assert count_words('one two three') == 3
        assert count_words('single') == 1
    
    def test_empty_string(self):
        """Test counting words in an empty string."""
        assert count_words('') == 0
    
    def test_whitespace_handling(self):
        """Test proper handling of various whitespace scenarios."""
        assert count_words('  spaces  ') == 1
        assert count_words('  multiple   spaces   between  ') == 3
        assert count_words('   ') == 0  # Only whitespace
        assert count_words('\t\n\r') == 0  # Various whitespace characters
    
    def test_punctuation_stripping(self):
        """Test that punctuation is properly stripped."""
        assert count_words('hello, world!') == 2
        assert count_words('test... more?') == 2
        assert count_words('(parentheses) [brackets]') == 2
        assert count_words('"quoted" text') == 2
    
    def test_punctuation_only(self):
        """Test strings with only punctuation."""
        assert count_words('!@#$%') == 0
        assert count_words('... --- ???') == 0
    
    def test_mixed_content(self):
        """Test mixed content with words, punctuation, and whitespace."""
        assert count_words('  hello,   world!  ') == 2
        assert count_words('one... two??? three!!!') == 3
        assert count_words('a, b; c: d.') == 4
    
    def test_edge_cases(self):
        """Test various edge cases."""
        assert count_words('a') == 1
        assert count_words('!') == 0
        assert count_words('a!') == 1
        assert count_words('!a') == 1
        assert count_words('!a!') == 1
