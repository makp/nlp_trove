"""
Tokenize text and run some common preprocessing tasks.

Notes:
- Don't forget to download the spaCy model.
"""

import spacy


class TextTokenizer:
    """Class for tokenizing text."""

    def __init__(self, model='en_core_web_trf'):
        """Initialize the TextTokenizer class."""
        self.nlp = spacy.load(model)
        self.custom_stopwords = set('would could may might account et al used also'.split(' ')) # noqa
        self.stopwords = self.nlp.Defaults.stop_words.union(
            self.custom_stopwords)

    def remove_stop_words(self, tokens):
        """Remove stopwords from the given list of tokens."""
        return [t for t in tokens if t.lower() not in self.stopwords]

    def remove_short_and_long_tokens(self, tokens,
                                     min_length=1,
                                     max_length=15):
        """
        Remove short and long tokens from the given list of tokens.

        The motivation for removing long tokens is that they could be
        artifacts of malformed data. And single character tokens are
        unlikely to be useful for downstream NLP tasks.
        """
        return [t for t in tokens
                if len(t) > min_length and len(t) <= max_length]

    def tokenize_text(self, text):
        """
        Preprocesse the given text.

        Return a list of spaCy Token objects.

        Steps:
        1. Lowercase and tokenize
        2. Lemmatize
        3. Remove stop words
        4. Remove short and long tokens
        """
        doc = self.nlp(text.lower())
        tokens = [token.lemma_ for token in doc if
                  not token.is_space and
                  not token.is_punct]
        tokens = self.remove_stop_words(tokens)
        tokens = self.remove_short_and_long_tokens(tokens)
        return tokens

