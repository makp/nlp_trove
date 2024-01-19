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
            # partial(tp.replace.phone_numbers, repl=" _PHONE_ "),
            # partial(tp.replace.numbers, repl=""),
            partial(tp.replace.currency_symbols, repl=" _CURRENCY_ "))

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

    def clean_text(self, text):
        """Clean text."""
        text = self.normalize_text(text)
        text = self.replace_from_text(text)
        return tp.normalize.whitespace(text)


class TextSplitter:
    """Class for splitting text by using regexes."""

    def __init__(self):
        """Initialize the TextSplitter class."""
        # Regexes
        self.RE_SUSPICIOUS = r"([^a-zA-Z'\s-]+)"
        self.RE_TOKEN = r"([a-zA-Z]+(?:-[a-zA-Z]+)*)"

    def add_space_after(self, text):
        """Add a space after certain symbols."""
        pattern = r"([.,;:!?\)\]/]+)(\w+)"
        return re.sub(pattern, r"\1 \2", text)

    def add_space_before(self, text):
        """Add a space before certain symbols."""
        pattern = r"(\w+)([\[\(/]+)"
        return re.sub(pattern, r"\1 \2", text)

    def surround_suspicious_chars_with_spaces(self, text):
        """Surround suspicious characters within words with spaces."""
        pattern = f"{self.RE_TOKEN}{self.RE_SUSPICIOUS}{self.RE_TOKEN}"
        return re.sub(pattern, r"\1 \2 \3", text)

    def remove_numbers_before(self, text):
        """
        Replace numbers before non-digits with a space.

        But only replace if there are at least two alphabetic characters.
        """
        pattern = r"\d+([a-zA-Z]{2,})"
        text = re.sub(pattern, r" \1", text)
        return text

    def remove_numbers_after(self, text):
        """Replace numbers after non-digits with a space."""
        pattern = self.RE_TOKEN + r"\d+"
        text = re.sub(pattern, r"\1 ", text)
        return text

    def remove_hyphens(self, text):
        """Replace hyphens with space."""
        pattern = r"-+|‐+"
        return re.sub(pattern, " ", text)

    def remove_quotes_and_apostrophes(self, text):
        """Replace quotes and apostrophes with a space."""
        pattern = r"['\"]+"
        return re.sub(pattern, r" ", text)

    def use_uppercase_to_split_words(self, text):
        """
        Use uppercase to separate words.

        Make sure the capital letter is preceded by a lowercase
        letter before adding space. Accordingly, this function
        incorrectly split words such as `iPhone`.
        """
        pattern = r"([a-z])([A-Z])"
        return re.sub(pattern, r"\1 \2", text)

    def split_text(self, text):
        """Split text."""
        text = self.add_space_after(text)
        text = self.add_space_before(text)
        text = self.surround_suspicious_chars_with_spaces(text)
        text = self.remove_numbers_before(text)
        text = self.remove_numbers_after(text)
        text = self.remove_hyphens(text)
        text = self.remove_quotes_and_apostrophes(text)
        text = self.use_uppercase_to_split_words(text)
        return tp.normalize.whitespace(text)
