"""
Routines to filter tokens.

TODO:
- Consider using spaCy dependency tags to filter out tokens. spaCy
  dependency tags seems to be derived from the Universal Dependencies
  project.
"""

import spacy
from vectorization.sparse_vectorization import build_tfidf_vectors

# Load spaCy model
nlp = spacy.load('en_core_web_trf')


def convert_to_spacy_doc(tokenized_doc,
                         disabled_components=['ner',
                                              'lemmatizer']):
    """Convert a list of tokens to a spaCy Doc."""
    doc = spacy.tokens.Doc(nlp.vocab, words=tokenized_doc)
    for name, proc in nlp.pipeline:
        if name not in disabled_components:
            doc = proc(doc)
    return doc


def filter_tokens_with_pos(tokenized_doc):
    """Filter tokens based on spaCy POS tags."""
    doc = convert_to_spacy_doc(tokenized_doc)
    pos_tags = {'NOUN', 'PROPN', 'VERB', 'ADJ'}
    return [t.text for t in doc
            if t.pos_ in pos_tags]


class FilterTokensWithTFIDF:
    """Filter tokens based on their TF-IDF scores."""

    def __init__(self, tokenized_docs, threshold=0.1):
        """Initialize the FilterTokensWithTFIDF class."""
        self.tokenized_docs = tokenized_docs
        self.dictionary, self.tfidf_vecs = build_tfidf_vectors(
            tokenized_docs)
        self.threshold = threshold
        self.tokens_to_keep = self.get_tokens_above_tfidf_score()

    def get_tokens_above_tfidf_score(self):
        """Return tokens above a certain TF-IDF score."""
        tokens_to_keep = set()
        for doc_vec in self.tfidf_vecs:
            for token_id, score in doc_vec:
                if score > self.threshold:
                    tokens_to_keep.add(self.dictionary[token_id])
        return tokens_to_keep

    def filter_doc(self, tokenized_doc):
        """Filter tokens based on a list of tokens to keep."""
        return [token for token in tokenized_doc
                if token in self.tokens_to_keep]
