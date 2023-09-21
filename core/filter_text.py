from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from langdetect import detect_langs
import re


def detect_language(text):
    if not isinstance(text, str) or text.strip() == '':
        return None
    try:
        return detect(text)
    except LangDetectException:
        return None


def is_english(text):
    lang = detect_language(text)
    return lang == 'en'


def detect_language_distribution(text):
    """
    Detects the language distribution of a given text using the
    langdetect library.

    Args:
    - text (str): The text to detect the language distribution of.

    Returns:
    - lang_prob (dict): A dictionary containing the detected languages
      as keys and their probabilities as values.
    """
    langs = detect_langs(text)
    lang_prob = {lang.lang: round(lang.prob, 2) for lang in langs}
    return lang_prob


def get_number_of_words(text):
    """Count the number of words in a string."""
    if not isinstance(text, str):
        return 0
    words = re.findall(r'\b\w+\b', text)
    return len(words)
