"""Utility functions for parity operations."""


def is_even(n: int) -> bool:
    """Check if a number is even.
    
    Args:
        n: The integer to check for evenness.
        
    Returns:
        True if the number is divisible by 2, False otherwise.
        
    Examples:
        >>> is_even(4)
        True
        >>> is_even(3)
        False
        >>> is_even(0)
        True
        >>> is_even(-2)
        True
        >>> is_even(-1)
        False
    """
    return n % 2 == 0
