"""Tests for parity utility functions."""

import pytest
from src.parity_utils import is_even


class TestIsEven:
    """Test cases for the is_even function."""
    
    def test_even_positive_numbers(self):
        """Test that positive even numbers return True."""
        assert is_even(2) == True
        assert is_even(4) == True
        assert is_even(100) == True
        assert is_even(1000) == True
    
    def test_odd_positive_numbers(self):
        """Test that positive odd numbers return False."""
        assert is_even(1) == False
        assert is_even(3) == False
        assert is_even(99) == False
        assert is_even(1001) == False
    
    def test_zero(self):
        """Test that zero returns True."""
        assert is_even(0) == True
    
    def test_negative_even_numbers(self):
        """Test that negative even numbers return True."""
        assert is_even(-2) == True
        assert is_even(-4) == True
        assert is_even(-100) == True
    
    def test_negative_odd_numbers(self):
        """Test that negative odd numbers return False."""
        assert is_even(-1) == False
        assert is_even(-3) == False
        assert is_even(-99) == False
    
    def test_acceptance_criteria(self):
        """Test the specific acceptance criteria."""
        assert is_even(4) == True
        assert is_even(3) == False
        assert is_even(0) == True
