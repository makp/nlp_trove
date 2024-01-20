"""Split tokens using SymSpell and spaCy."""

import spacy
from symspellpy.symspellpy import SymSpell
import pkg_resources


class SplitTokens:
    """Class for splitting tokens."""

    # Dictionary shipped with symspellpy
    path = pkg_resources.resource_filename(
        "symspellpy", "frequency_dictionary_en_82_765.txt")

    # Tell whether GPU is available
    print("GPU available:", spacy.prefer_gpu())

    def __init__(self, path_dict=path):
        """Initialize the SplitTokens class."""
        # Set up SymSpell
        self.sym_spell = SymSpell()
        if self.sym_spell.load_dictionary(
                path_dict, term_index=0, count_index=1):
            print("Dictionary loaded.")
        else:
            print("Dictionary failed to load.")

        # Initialize spaCy model
        self.nlp = spacy.load("en_core_web_trf")

    def update_dictionary(self, text):
        """Use text to update SymSpell dictionary."""
        doc = self.nlp.make_doc(text)
        for t in doc:
            # Check whether t is alpha and has a reasonable length
            if (t.is_alpha and (20 > len(t.text) > 2)):
                self.sym_spell.create_dictionary_entry(t.text, 1)

    def prudent_segment(self, token):
        """Prudent word segmentation on a spaCy Token."""
        # Run word segmentation without correcting words
        seg_token = self.sym_spell.word_segmentation(
            token.text, max_edit_distance=0)

        # Are all segments in the dictionary?
        segs_in_dict = all(part in self.sym_spell.words for
                           part in seg_token.corrected_string.split())

        if segs_in_dict:        # or (len(token.text) > 20)
            return seg_token.corrected_string + token.whitespace_
        else:
            return token.text_with_ws

    def fix_word_segmentation(self, text, cautious=True):
        """Fix word segmentation."""
        # Process text with spaCy
        doc = self.nlp(text)

        # Create list to store tokens
        lst_tokens = []

        for t in doc:
            if (t.is_alpha and
               (t.ent_type == 0) and  # not an entity
               {t.lemma_.lower(), t.text.lower(), t.lemma_, t.text}.\
               isdisjoint(set(self.sym_spell.words.keys()))):
                if cautious:
                    lst_tokens.append(self.prudent_segment(t))
                else:
                    seg_token = self.sym_spell.word_segmentation(t.text)
                    lst_tokens.append(
                        seg_token.corrected_string + t.whitespace_)
            else:
                lst_tokens.append(t.text_with_ws)

        return "".join(lst_tokens)
