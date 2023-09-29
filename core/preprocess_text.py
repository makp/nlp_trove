import re


# NLP modules
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.util import bigrams


# Regex for matching punctuation characters
PUNCT_RE = re.compile(r'^[^a-zA-Z]+|[^a-zA-Z]+$')


class TextPreprocessor:
    """
    A class used to preprocess text data for NLP tasks.
    """
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def download_nltk_data(self):
        """
        Downloads required NLTK data for preprocessing.
        """
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')

    def lowercase_and_tokenize_text(self, text):
        """
        Tokenizes and lowercases the given text.

        Parameters
        ----------
        text : str
            The text to tokenize and lowercase.

        Returns
        -------
        list of str
            The list of tokens.
        """
        return word_tokenize(text.lower())

    def is_punct(self, token):
        """
        Check for punctuation characters at the beginning and at end of a
        string.
        """
        return PUNCT_RE.search(token) is not None

    def remove_punctuation(self, tokens):
        """
        Removes punctuation characters from the given list of tokens.

        Parameters
        ----------
        tokens : list of str
            The list of tokens to remove punctuation from.

        Returns
        -------
        list of str
            The list of tokens with punctuation removed.
        """
        return [token for token in tokens if not self.is_punct(token)]

    def remove_stop_words(self, tokens):
        """
        Removes stop words from the given list of tokens.

        Parameters
        ----------
        tokens : list of str
            The list of tokens to remove stop words from.

        Returns
        -------
        list of str
            The list of tokens with stop words removed.
        """
        return [word for word in tokens if word not in self.stop_words]

    def lemmatize(self, tokens):
        """
        Lemmatizes the given list of tokens.

        Parameters
        ----------
        tokens : list of str
            The list of tokens to lemmatize.

        Returns
        -------
        list of str
            The list of lemmatized tokens.
        """
        return [self.lemmatizer.lemmatize(token) for token in tokens]

    def remove_single_characters(self, tokens):
        """
        Removes single characters from the given list of tokens.

        Parameters
        ----------
        tokens : list of str
            The list of tokens to remove single characters from.

        Returns
        -------
        list of str
            The list of tokens with single characters removed.
        """
        return [token for token in tokens if len(token) > 1]

    def generate_bigrams(self, tokens):
        """
        Generates bigrams from the given list of tokens.

        Parameters
        ----------
        tokens : list of str
            The list of tokens to generate bigrams from.

        Returns
        -------
        list of str
            The list of bigrams.
        """
        return ['_'.join(bigram) for bigram in bigrams(tokens)]

    def preprocess_text(self, text, create_bigrams=True):
        """
        Preprocesses the given text by performing the following steps:
        1. Tokenizes and lowercases the text.
        2. Removes punctuation characters.
        3. Removes stop words
        4. Removes single characters.
        5. Lemmatizes.
        6. Generates bigrams (if bigrams=True).

        Parameters
        ----------
        text : str
            The text to preprocess.
        bigrams : bool, optional
            Whether or not to generate bigrams (default is True).

        Returns
        -------
        list of str
            The list of preprocessed tokens (and bigrams, if applicable).
        """
        tokens = self.lowercase_and_tokenize_text(text)
        tokens = self.remove_punctuation(tokens)
        tokens = self.remove_stop_words(tokens)
        tokens = self.remove_single_characters(tokens)
        tokens = self.lemmatize(tokens)
        if create_bigrams:
            b_tokens = self.generate_bigrams(tokens)
            return tokens + b_tokens
        else:
            return tokens


