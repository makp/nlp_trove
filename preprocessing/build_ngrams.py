"""Build n-grams from a list of tokenized documents."""

from gensim.models.phrases import Phrases, Phraser, ENGLISH_CONNECTOR_WORDS


def train_phrase_model(tokenized_docs,
                       min_count=5,
                       threshold=10):
    """
    Train a phrase model on a list of tokenized docs.

    Note on the parameters:
    - `min_cont`: Specifices the minimum number of times a bigram must
      appear. Accordingly, a higher value for this parameter means
      fewer bigrams.
    - `threshold`: Speficies how strong the relationship between two
      words must be to be considered a bigram. Accordingly, a higher
      threshold means fewer bigrams.
    """
    phrase_model = Phraser(Phrases(tokenized_docs,
                                   min_count=min_count,
                                   threshold=threshold,
                                   connector_words=ENGLISH_CONNECTOR_WORDS))
    return phrase_model
