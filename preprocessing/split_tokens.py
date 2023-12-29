"""Split tokens using SymSpell and spaCy."""

import spacy
import re
from symspellpy.symspellpy import SymSpell
import pkg_resources


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
            # Check if t is alphanumeric and not in the dictionary
            if ((re.match(self.pattern, t.text) and
                 (t.text not in self.sym_spell.words))):

                # Run SymSpell word segmentation
                segmented_token = self.sym_spell.word_segmentation(
                    t.text, max_edit_distance=max_edit_distance)

                # Don't correct words and only accept segments if both
                # segments are in the dictionary
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

        return "".join(lst_tokens)
