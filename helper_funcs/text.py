"""Text processing utilities."""

import re


def tokenize_with_regex(text):
    """Tokenize text using regex."""
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    return re.findall(r"\b\w+\b", text)


def search_for_long_words(text, min_length=15):
    """Search for long words in a string."""
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    # `{{` denotes a literal `{` inside an f-string.
    long_words = re.findall(rf"\b\w{{{min_length},}}\b", text)
    return long_words
