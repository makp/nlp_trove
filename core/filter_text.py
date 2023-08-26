from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException


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


def has_min_words(text, min_words):
    if not isinstance(text, str):
        return False
    num_words = len(text.split())
    return num_words >= min_words
