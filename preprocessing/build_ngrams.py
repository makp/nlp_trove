"""Build n-grams from a list of tokenized documents."""

from gensim.models.phrases import ENGLISH_CONNECTOR_WORDS, Phraser, Phrases


def train_phrase_model(tokenized_docs, min_count=5, threshold=10):
    """
    Train a phrase model on a list of tokenized docs.

    Note on the parameters:
    - `min_cont`: Minimum number of times a word must appear to be considered
      by the model. A higher value means fewer bigrams.
    - `threshold`: Specifies how strong the relationship between two words must
      be to be considered a bigram. A higher threshold means fewer bigrams.
    """
    phrase_model = Phraser(
        Phrases(
            tokenized_docs,
            min_count=min_count,
            threshold=threshold,
            connector_words=ENGLISH_CONNECTOR_WORDS,
        )
    )
    return phrase_model
