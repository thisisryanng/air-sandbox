"""Utility functions for string reversal operations."""


def reverse_string(s: str) -> str:
    """Reverse a string.
    
    Args:
        s: The input string to reverse.
        
    Returns:
        The reversed string.
        
    Examples:
        >>> reverse_string('hello')
        'olleh'
        >>> reverse_string('')
        ''
        >>> reverse_string('a')
        'a'
    """
    return s[::-1]
