"""Split tokens using SymSpell and spaCy."""

import spacy
from symspellpy.symspellpy import SymSpell
import pkg_resources


class SplitTokens:
    """Class for splitting tokens."""

    # Dictionary shipped with symspellpy
    path = pkg_resources.resource_filename(
        "symspellpy", "frequency_dictionary_en_82_765.txt")

    def __init__(self, path_dict=path):
        """Initialize the SplitTokens class."""
        # Set up SymSpell
        self.sym_spell = SymSpell()
        if self.sym_spell.load_dictionary(
                path_dict, term_index=0, count_index=1):
            print("Dictionary loaded.")
        else:
            print("Dictionary failed to loaded.")

        # Initialize spaCy model
        self.nlp = spacy.load("en_core_web_trf")

    def update_dictionary(self, text):
        """Use text to update SymSpell dictionary."""
        doc = self.nlp.make_doc(text)
        for t in doc:
            # Check whether t is alpha and has a reasonable length
            if (t.is_alpha and (18 > len(t.text) > 2)):
                self.sym_spell.create_dictionary_entry(t.text, 1)

    def fix_word_segmentation(self, text):
        """Fix word segmentation."""
        # Tokenize text with spaCy
        doc = self.nlp(text)

        # Create list to store tokens
        lst_tokens = []

        for t in doc:
            if (t.is_alpha and
               (t.ent_type == 0) and  # not an entity
               (t.lemma_.lower() not in self.sym_spell.words)):

                # Run SymSpell word segmentation but don't correct words
                seg_token = self.sym_spell.word_segmentation(
                    t.text, max_edit_distance=0)

                # Only accept segments if all of them are in the dictionary
                if all(part in self.sym_spell.words for
                       part in seg_token.corrected_string.split()):
                    # (seg_token.corrected_string.replace(" ", "") == t.text)

                    # Save segmented token
                    lst_tokens.append(
                        seg_token.corrected_string + t.whitespace_)
                else:
                    lst_tokens.append(t.text_with_ws)
            else:
                lst_tokens.append(t.text_with_ws)

        return "".join(lst_tokens)
