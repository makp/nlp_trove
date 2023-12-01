"""
Routines to filter tokens.

TODO:
- Consider using spaCy dependency tags to filter out tokens. spaCy
  dependency tags seems to be derived from the Universal Dependencies
  project.
"""

import spacy

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


def get_tokens_above_tfidf_score(dictionary, tfidf_vecs,
                                 threshold=0.1):
    """Return tokens above a certain TF-IDF score."""
    tokens_to_keep = set()
    for doc_vec in tfidf_vecs:
        for token_id, score in doc_vec:
            if score > threshold:
                tokens_to_keep.add(dictionary[token_id])
    return tokens_to_keep


def filter_tokens(tokenized_doc, tokens_to_keep):
    """Filter tokens based on a list of tokens to keep."""
    return [token for token in tokenized_doc
            if token in tokens_to_keep]
