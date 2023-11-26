"""Transform text into sparse vectors."""

from gensim.corpora import Dictionary


def map_tokens_to_integer_ids(tokenized_docs,
                              min_doc_freq=25,
                              max_doc_frac=0.9):
    """
    Build a dictionary from tokenized documents.

    When building a dictionary, filter out frequent and infrequent
    tokens.
    """
    # Create a dictionary
    id2word = Dictionary(tokenized_docs)

    # Filter out certain tokens
    id2word.filter_extremes(no_below=min_doc_freq,
                            no_above=max_doc_frac)

    return id2word
