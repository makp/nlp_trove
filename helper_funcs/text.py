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


def get_percentage_in_dictionary(text, dictionary):
    """Get percentage of words in a text that are in a dictionary."""
    if not isinstance(text, str):
        raise ValueError("Input must be a string.")
    if not isinstance(dictionary, set):
        raise ValueError("Dictionary must be a set.")
    words = tokenize_with_regex(text.lower())
    num_words_in_dict = sum(word in dictionary for word in words)
    return num_words_in_dict / len(words) if words else 0
