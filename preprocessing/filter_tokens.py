"""Routines to filter tokens."""

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
    """Filter words based on spaCy POS tags."""
    doc = convert_to_spacy_doc(tokenized_doc)
    pos_tags = ['NOUN', 'PROPN', 'VERB', 'ADJ']
    return [t.text for t in doc if t.pos_ in pos_tags]
