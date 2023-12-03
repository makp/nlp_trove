"""
Text summarization.

Algorithms:
- LSA
- TextRank
- TF-IDF

Notes:
- `TextRank` seems better suited for longer texts. This might be
  because `TextRank` needs larger graphs to do its magic.
"""

from vectorization.sparse_vectorization import build_tfidf_vectors
from preprocessing.clean_text import TextCleaner
from preprocessing.tokenize_text import TextTokenizer

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from heapq import nlargest


class TextSummarizer:
    """Summarize text."""

    def __init__(self, text):
        """Initialize the TextSummarizer class."""
        self.stemmer = Stemmer('english')
        self.sumy_tokenizer = Tokenizer('english')

        # Initialize sumy summarizers
        self.sumy_summarizer_lsa = LsaSummarizer(self.stemmer)
        self.sumy_summarizer_textrank = TextRankSummarizer(self.stemmer)

        # Set stop words
        self.sumy_summarizer_lsa.stop_words = get_stop_words('english')
        self.sumy_summarizer_textrank.stop_words = get_stop_words('english')

        # Parse text
        self.parser = PlaintextParser.from_string(text, self.sumy_tokenizer)
        self.sentences = [str(sent) for sent in self.parser.document.sentences]

    def summarize_text_with_lsa(self, num_sentences=2):
        """Summarize the given text with LSA."""
        return [str(sent) for sent in self.sumy_summarizer_lsa(
            self.parser.document, num_sentences)]

    def summarize_text_with_textrank(self, num_sentences=2):
        """Summarize the given text with TextRank."""
        return [str(sent) for sent in self.sumy_summarizer_textrank(
            self.parser.document, num_sentences)]

    def summarize_text_with_tfidf(self, num_sentences=2):
        """Summarize the given text with TF-IDF."""
        # Extract tokens
        cleaner = TextCleaner()
        tokenizer = TextTokenizer()
        tokenized_sentences = [cleaner.clean_text(sent)
                               for sent in self.sentences]
        tokenized_sentences = [tokenizer.tokenize_text(sent)
                               for sent in tokenized_sentences]

        # Build TF-IDF vectors
        _, tfidf_vecs = build_tfidf_vectors(tokenized_sentences)

        # Sum tfidf scores for each sentence
        def sum_tfidf_scores(doc_vec):
            return sum([score for _, score in doc_vec])

        sentence_scores = [(i, sum_tfidf_scores(doc_vec))
                           for i, doc_vec in enumerate(tfidf_vecs)]

        top_indices = nlargest(num_sentences, sentence_scores,
                               key=lambda x: x[1])

        # Return top sentences
        return [self.sentences[i] for i, _ in top_indices]
