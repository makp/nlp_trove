"""Clean text."""

import html
import textacy.preprocessing as tp
from functools import partial
from bs4 import BeautifulSoup, Comment
import re


class TextCleaner:
    """Class for cleaning text."""

    def __init__(self):
        """Initialize the TextCleaner class."""
        self.normalize_text = tp.make_pipeline(
            tp.normalize.bullet_points,
            tp.normalize.hyphenated_words,  # reattach separated by line breaks
            tp.normalize.quotation_marks,
            tp.normalize.unicode,
            tp.remove.accents)

        self.replace_from_text = tp.make_pipeline(
            partial(tp.replace.urls, repl=" _URL_ "),
            partial(tp.replace.emails, repl=" _EMAIL_ "),
            partial(tp.replace.phone_numbers, repl=" _PHONE_ "),
            # partial(tp.replace.numbers, repl=""),
            partial(tp.replace.currency_symbols, repl=" _CURRENCY_ "))

    def remove_numbers_before(self, text):
        """Replace numbers before non-digits with a space."""
        pattern = r"(\d+)([^\d\s]+)"
        # '(\d+)' matches one or more digits
        # '([^\d\s]+)' matches one or more non-digit and
        # non-whitespace
        text = re.sub(pattern, r' \2', text)
        return text

    def remove_numbers_after(self, text):
        """Replace numbers after non-digits with a space."""
        pattern = r"([^\d\s]+)(\d+)"
        text = re.sub(pattern, r'\1 ', text)
        return text

    def clean_html(self, text):
        """Clean HTML text."""
        text = html.unescape(text)  # convert html escape to characters

        # parse HTML
        soup = BeautifulSoup(text, 'lxml')

        # remove certain tags
        for tag in soup(["script", "style"]):
            tag.decompose()

        # remove comments
        for comment in soup.find_all(
                string=lambda t: isinstance(t, Comment)):
            comment.extract()  # comment doesn't have decompose() method

        # get text and add a space between tags
        text = soup.get_text(" ")

        return text

    def aggressive_clean(self, text, is_html=False):
        """
        More aggressive cleaning.

        Steps:
        - Normalize text.
        - Replace certain types of text (e.g. URLs, emails,
          and phone numbers).
        - Normalize whitespace.
        """
        if is_html:
            text = self.clean_html(text)
        text = self.normalize_text(text)
        text = self.replace_from_text(text)
        text = self.remove_numbers_before(text)
        text = self.remove_numbers_after(text)
        return tp.normalize.whitespace(text)
