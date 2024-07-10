"""Build n-grams from a list of tokenized documents."""

from gensim.models.phrases import ENGLISH_CONNECTOR_WORDS, Phrases


def train_phrase_model(
    tokenized_docs,
    min_count=5,
    threshold=0.7,
    scoring="npmi",
):
    """
    Train a phrase model on a list of tokenized docs.

    Note on the parameters:
    - `min_cont`: Minimum number of times a word must appear to be considered
      by the model. A higher value means fewer bigrams.
    - `threshold`: Specifies how strong the relationship between two words must
      be to be considered a bigram. A higher threshold means fewer bigrams. For
      npmi scoring, the threshold should be between -1 and +1.
    """
    phrase_model = Phrases(
        tokenized_docs,
        min_count=min_count,
        threshold=threshold,
        connector_words=ENGLISH_CONNECTOR_WORDS,
        scoring=scoring,
    )

    return phrase_model.freeze()
