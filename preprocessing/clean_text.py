"""Clean text."""

import html
import textacy.preprocessing as tp
from bs4 import BeautifulSoup, Comment


class TextCleaner:
    """Class for cleaning text."""

    def __init__(self):
        """Initialize the TextCleaner class."""
        self.normalize_text = tp.make_pipeline(
            tp.normalize.bullet_points,
            tp.normalize.hyphenated_words,  # reattach separated by line breaks
            tp.normalize.quotation_marks,
            tp.normalize.unicode)

        self.replace_from_text = tp.make_pipeline(
            tp.replace.urls,
            tp.replace.emails,
            tp.replace.phone_numbers,
            tp.replace.numbers,
            tp.replace.currency_symbols)

        self.remove_from_text = tp.make_pipeline(
            tp.remove.accents,
            tp.remove.punctuation)

    def clean_html(self, text):
        """Clean HTML text."""
        text = html.unescape(text)  # convert html escape to characters

        # parse HTML
        soup = BeautifulSoup(text, 'lxml')

        # remove certain tags
        for tag in soup(["script", "style"]):
            tag.decompose()

        # remove comments
        for comment in soup.find_all(string=lambda t:
                                        isinstance(t, Comment)):
            comment.extract()  # comment doesn't have decompose() method

        # get untagged text
        text = soup.get_text()

        return text

    def clean_text(self, text, is_html=False):
        """Clean text."""
        if is_html:
            text = self.clean_html(text)
        text = self.normalize_text(text)
        text = self.replace_from_text(text)
        text = self.remove_from_text(text)
        text = tp.normalize.whitespace(text)
        return text
