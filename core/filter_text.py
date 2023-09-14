from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
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


def get_number_of_words(text):
    """Count the number of words in a string."""
    if not isinstance(text, str):
        return 0
    words = re.findall(r'\b\w+\b', text)
    return len(words)
