"""Text processing utilities."""

import re


def get_number_of_words(text):
    """Count the number of words in a string."""
    if not isinstance(text, str):
        return 0
    words = re.findall(r'\b\w+\b', text)
    return len(words)
