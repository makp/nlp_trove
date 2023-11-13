"""Build n-grams from a list of tokenized documents."""

from gensim.models.phrases import Phrases, Phraser, ENGLISH_CONNECTOR_WORDS


def train_phrase_model(tokenized_docs,
                       min_count=5,
                       threshold=10):
    """Train a phrase model on a list of tokenized docs."""
    phrase_model = Phraser(Phrases(tokenized_docs,
                                   min_count=min_count,
                                   threshold=threshold,
                                   connector_words=ENGLISH_CONNECTOR_WORDS))
    return phrase_model


def apply_phrase_model(tokenized_docs, phrase_model):
    """Apply the phrase model to a list of tokenized docs."""
    return [phrase_model[doc] for doc in tokenized_docs]
