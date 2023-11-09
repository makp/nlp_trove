"""Preprocess a collection of (raw) documents."""

from preprocessing.preprocess_text import TextPreprocessor


# Initialize the TextPreprocessor class
preprocessor = TextPreprocessor()


def preprocess_docs(docs):
    """
    Preprocess a collection of raw documents.

    The preprocessing involves training a phrase model to detect bigrams.

    Parameters
    ----------
    docs : list of str
        A list of raw docs to be preprocessed.

    Returns
    -------
    list of list of str
        A list of lists containing preprocessed tokens for each text.
    """
    # Preprocess docs without bigrams for training
    tokenized_docs = [preprocessor.preprocess_text(text, create_bigrams=False)
                      for text in docs]

    # Train the bigram model
    preprocessor.train_phrase_model(tokenized_docs)

    # Preprocess the docs with bigrams
    preprocessed_docs = [preprocessor.preprocess_text(text) for text in docs]

    return preprocessed_docs
