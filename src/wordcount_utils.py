"""Word counting utilities module."""

import string


def count_words(text: str) -> int:
    """Count the number of words in a text string.
    
    Words are defined as sequences of characters separated by whitespace.
    Punctuation is stripped from each word before counting.
    
    Args:
        text (str): The input text to count words in.
        
    Returns:
        int: The number of words found in the text.
        
    Examples:
        >>> count_words('hello world')
        2
        >>> count_words('  spaces  ')
        1
        >>> count_words('')
        0
    """
    if not text:
        return 0
    
    # Split on whitespace to get potential words
    words = text.split()
    
    # Strip punctuation from each word and filter out empty strings
    cleaned_words = []
    for word in words:
        # Remove punctuation from both ends of the word
        cleaned_word = word.strip(string.punctuation)
        if cleaned_word:  # Only count non-empty words after cleaning
            cleaned_words.append(cleaned_word)
    
    return len(cleaned_words)
