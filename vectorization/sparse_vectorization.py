"""Transform text into sparse vectors."""

from gensim.corpora import Dictionary
from gensim.models import TfidfModel


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


def build_tfidf_vectors(tokenized_docs, id2word):
    """Build TF-IDF vectors from tokenized documents."""
    # Convert tokenized documents into bow vectors
    bow_corpus = [id2word.doc2bow(doc) for doc in tokenized_docs]

    # Fit the TF-IDF model
    tfidf = TfidfModel(dictionary=id2word)

    # Return corpus as TF-IDF vectors
    return tfidf[bow_corpus]
