"""
Run common text preprocessing steps.

Notes:
- Don't forget to download the spaCy model with conda:
  `conda install -c conda-forge en_core_web_trf`
"""

import spacy
from gensim.models.phrases import Phrases, Phraser


# Load spaCy model
nlp = spacy.load('en_core_web_trf', disable=['parser', 'ner'])


# stopwords
CUSTOM_STOP_WORDS = set('would could may might account et al used also'.split(' ')) # noqa
STOP_WORDS = nlp.Defaults.stop_words.union(CUSTOM_STOP_WORDS)


class TextTokenizer:
    """Class for preprocessing text data for NLP tasks."""

    def __init__(self):
        """Initialize the TextTokenizer class."""
        self.phrase_model = None  # initialize model

    def train_phrase_model(self, sentences):
        """
        Train a phrase detection model using Gensim's Phrases.

        Parameters
        ----------
        sentences : list of list of str
            A list of tokenized sentences for training the phrase
            model.
        """
        self.phrase_model = Phraser(Phrases(sentences,
                                            min_count=5,
                                            threshold=10))

    def remove_stop_words(self, tokens):
        """
        Remove stopwords from the given list of tokens.

        Parameters
        ----------
        tokens : list of str
            The list of tokens to remove stop words from.

        Returns
        -------
        list of str
            The list of tokens with stop words removed.
        """
        return [word for word in tokens if word.lower() not in STOP_WORDS]

    def remove_short_and_long_tokens(self, tokens,
                                     min_length=1,
                                     max_length=15):
        """
        Remove short and long tokens from the given list of tokens.

        The motivation for removing long tokens is that they could be
        artifacts of malformed data. And single character tokens are
        unlikely to be useful for downstream NLP tasks.
        """
        return [token for token in tokens
                if len(token) > min_length and len(token) <= max_length]

    def preprocess_text(self, text, create_bigrams=True):
        """
        Preprocesse the given text.

        Steps:
        1. Tokenize the text using spaCy.
        2. Lemmatize
        3. Remove stop words
        4. Remove short and long tokens
        5. Generate bigrams (if `create_bigrams=True`).

        Parameters
        ----------
        text : str
            The text to preprocess.
        create_bigrams : bool, optional
            Whether or not to generate bigrams (default is True).

        Returns
        -------
        list of str
            The list of preprocessed tokens (and bigrams, if
            applicable).
        """
        doc = nlp(text.lower())
        tokens = [token.lemma_ for token in doc if
                  not token.is_space and
                  not token.is_punct]
        tokens = self.remove_stop_words(tokens)
        tokens = self.remove_short_and_long_tokens(tokens)
        if create_bigrams and self.phrase_model:
            tokens = self.phrase_model[tokens]
        return tokens