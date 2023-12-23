"""Transform text into sparse vectors."""

from gensim.corpora import Dictionary
from gensim.models import TfidfModel


def map_tokens_to_integer_ids(tokenized_docs,
                              no_below=1,
                              no_above=1,
                              keep_n=None):
    """
    Build a dictionary from tokenized documents.

    When building a dictionary, filter out frequent and infrequent
    tokens. The keyword argument `no_below` is an absolute number and
    `no_above` is a fraction of the total corpus size. Keep `keep_n`
    most frequent tokens after the above filtering.
    """
    # Create a dictionary
    id2word = Dictionary(tokenized_docs)

    # Filter out certain tokens
    id2word.filter_extremes(no_below=no_below,
                            no_above=no_above,
                            keep_n=keep_n)

    return id2word


def build_bow_vectors(tokenized_docs,
                      no_below=1,
                      no_above=1,
                      keep_n=None):
    """Build bag-of-words vectors from tokenized documents."""
    id2word = map_tokens_to_integer_ids(tokenized_docs,
                                        no_below=no_below,
                                        no_above=no_above,
                                        keep_n=keep_n)

    # Convert tokenized documents into bow vectors
    bow_corpus = [id2word.doc2bow(doc) for doc in tokenized_docs]

    # Return dictionary and corpus as bow vecs
    return id2word, bow_corpus


def build_tfidf_vectors(tokenized_docs,
                        no_below=1,
                        no_above=1,
                        keep_n=None):
    """Build TF-IDF vectors from tokenized documents."""
    id2word, bow_corpus = build_bow_vectors(tokenized_docs,
                                            no_below=no_below,
                                            no_above=no_above,
                                            keep_n=keep_n)

    # Fit the TF-IDF model
    tfidf = TfidfModel(dictionary=id2word)

    # Return dictionary and corpus as TF-IDF vecs
    return id2word, tfidf[bow_corpus]
