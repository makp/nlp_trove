"""
Functions for filtering documents based on language.

Notes:
- Facebook's `fastText` library provides a pretrained model.
"""

from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from langdetect import detect_langs


def detect_language(text):
    """Return the language of the text."""
    if not isinstance(text, str) or text.strip() == '':
        return None
    try:
        return detect(text)
    except LangDetectException:
        return None


def is_english(text):
    """Check whether the text is written in English."""
    lang = detect_language(text)
    return lang == 'en'


def detect_language_distribution(text):
    """
    Perform language detection on the text.

    Args:
    text (str): The text for which to detect the language distribution.

    Returns:
    dict: A dictionary containing ISO language codes as keys and
        probabilities as values. The probabilities are rounded to two
        decimal places.
    """
    langs = detect_langs(text)
    lang_prob = {lang.lang: round(lang.prob, 2) for lang in langs}
    return lang_prob
