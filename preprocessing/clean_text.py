"""Clean text."""

import html
import textacy.preprocessing as tp
from functools import partial
from bs4 import BeautifulSoup, Comment
import spacy
import re
from symspellpy.symspellpy import SymSpell
import pkg_resources


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
        for comment in soup.find_all(string=lambda t:
                                     isinstance(t, Comment)):
            comment.extract()  # comment doesn't have decompose() method

        # get untagged text
        text = soup.get_text()

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

class SplitTokens:
    """Class for splitting tokens."""

    # Dictionary shipped with symspellpy
    path = pkg_resources.resource_filename(
        "symspellpy", "frequency_dictionary_en_82_765.txt")

    def __init__(self, path_dict=path):
        """Initialize the SplitTokens class."""
        # Define alphanumeric regex pattern
        self.pattern = r"^[a-zA-Z0-9]+$"

        # Initialize SymSpell
        self.sym_spell = SymSpell()
        if self.sym_spell.load_dictionary(
                path_dict, term_index=0, count_index=1):
            print("Dictionary loaded.")
        else:
            print("Dictionary failed to loaded.")

        # Initialize spaCy model
        self.nlp = spacy.load("en_core_web_trf",
                              disable=["parser", "ner"])

    def update_dictionary(self, text):
        """Use text to update SymSpell dictionary."""
        doc = self.nlp.make_doc(text)
        for t in doc:
            if (t.is_alpha and len(t.text) > 1):
                self.sym_spell.create_dictionary_entry(t.text, 1)

    def fix_word_segmentation(self, text, max_edit_distance=0):
        """Fix word segmentation."""
        # Tokenize text with spaCy
        doc = self.nlp.make_doc(text)

        # Create list to store tokens
        lst_tokens = []

        for t in doc:
            # Check if t.text is alphanumeric
            if (re.match(self.pattern, t.text) and (t.text not in self.sym_spell.words)):

                # Run SymSpell word segmentation
                segmented_token = self.sym_spell.word_segmentation(
                    t.text, max_edit_distance=max_edit_distance)

                # Don't correct words and only accept segments if both
                # words are in the dictionary
                if (segmented_token.corrected_string.replace(" ", "") == t.text
                    and all(part in self.sym_spell.words for
                            part in segmented_token.corrected_string.split())):

                    # Save segmented token
                    lst_tokens.append(
                        segmented_token.corrected_string + t.whitespace_)
                else:
                    lst_tokens.append(t.text + t.whitespace_)
            else:
                lst_tokens.append(t.text + t.whitespace_)
        text = self.remove_numbers_before_words(text)
        return tp.normalize.whitespace(text)
