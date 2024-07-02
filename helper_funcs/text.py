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


class CheckTextQuality:
    """Check text quality using different criteria."""

    def __init__(self, dictionary):
        """Initialize the CheckTextQuality class."""
        if not isinstance(dictionary, set):
            raise ValueError("Dictionary must be a set.")
        self.dictionary = dictionary
        self.min_length = 20

    def get_ratio_in_dictionary(self, text):
        """Get the ratio of words that are in the dictionary."""
        if not isinstance(text, str):
            raise ValueError("Input must be a string.")
        words = tokenize_with_regex(text.lower())
        num_words_in_dict = sum(word in self.dictionary for word in words)
        return num_words_in_dict / len(words) if words else 0

    def get_ratio_long_words(self, text):
        """Get the ratio of long words."""
        if not isinstance(text, str):
            raise ValueError("Input must be a string.")
        words = tokenize_with_regex(text.lower())
        long_words = search_for_long_words(text, self.min_length)
        return len(long_words) / len(words) if words else 0

    def check_quality_tokens(self, tokens):
        """Check the quality of a group of tokens."""
        num_tokens = len(tokens)
        num_words_in_dict = sum(token in self.dictionary for token in tokens)
        num_long_words = sum(len(token) > self.min_length for token in tokens)
        return num_words_in_dict / num_tokens, num_long_words / num_tokens
