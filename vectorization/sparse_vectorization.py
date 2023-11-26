"""Transform text into sparse vectors."""

from gensim.corpora import Dictionary
from gensim.models import TfidfModel


def map_tokens_to_integer_ids(tokenized_docs, no_below, no_above):
    """
    Build a dictionary from tokenized documents.

    When building a dictionary, filter out frequent and infrequent
    tokens.
    """
    # Create a dictionary
    id2word = Dictionary(tokenized_docs)

    # Filter out certain tokens
    id2word.filter_extremes(no_below=no_below,
                            no_above=no_above)

    return id2word


def build_tfidf_vectors(tokenized_docs,
                        no_below=10,
                        max_doc=0.9):
    """Build TF-IDF vectors from tokenized documents."""
    id2word = map_tokens_to_integer_ids(tokenized_docs,
                                        no_below=no_below,
                                        no_above=max_doc)

    # Convert tokenized documents into bow vectors
    bow_corpus = [id2word.doc2bow(doc) for doc in tokenized_docs]

    # Fit the TF-IDF model
    tfidf = TfidfModel(dictionary=id2word)

    # Return dictionary and corpus as TF-IDF vecs
    return id2word, tfidf[bow_corpus]
