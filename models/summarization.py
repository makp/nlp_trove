"""
Text summarization.

Notes:
- `TextRank` seems better suited for longer texts. This might be
  because `TextRank` needs larger graphs to do its magic.
"""

import spacy
import pytextrank               # noqa
from vectorization.sparse_vectorization import build_tfidf_vectors
from preprocessing.clean_text import TextCleaner
from preprocessing.tokenize_text import TextTokenizer


# Load spaCy model
nlp = spacy.load('en_core_web_trf')
nlp.add_pipe("textrank")


text = """
The curse of dimensionality refers to various phenomena that arise
when analyzing and organizing data in high-dimensional spaces that do
not occur in low-dimensional settings such as the three-dimensional
physical space of everyday experience. The expression was coined by
Richard E. Bellman when considering problems in dynamic programming.
Dimensionally cursed phenomena occur in domains such as numerical
analysis, sampling, combinatorics, machine learning, data mining and
databases. The common theme of these problems is that when the
dimensionality increases, the volume of the space increases so fast
that the available data become sparse. In order to obtain a reliable
result, the amount of data needed often grows exponentially with the
dimensionality. Also, organizing and searching data often relies on
detecting areas where objects form groups with similar properties; in
high dimensional data, however, all objects appear to be sparse and
dissimilar in many ways, which prevents common data organization
strategies from being efficient.
"""


def extract_key_phrases(text, num_phrases=5):
    """Extract key phrases from the given text."""
    doc = nlp(text)
    words = [(p.text, p.rank) for p in doc._.phrases]
    words = sorted(words, key=lambda x: x[1], reverse=True)
    return [word[0] for word in words[:num_phrases]]


def extract_sentences_and_tokens(text):
    """Extract sentences and tokens from the given text."""
    # Extract sentences
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    # Extract tokens
    cleaner = TextCleaner()
    tokenizer = TextTokenizer()
    tokenized_sentences = [cleaner.clean_text(sent) for sent in sentences]
    tokenized_sentences = [tokenizer.tokenize_text(sent)
                           for sent in tokenized_sentences]

    return sentences, tokenized_sentences


def summarize_text_with_tfidf(text, num_sentences=2):
    """Summarize the given text with TF-IDF."""
    # Extract sentences and tokens
    sentences, tokenized_sentences = extract_sentences_and_tokens(text)

    # Build TF-IDF vectors
    _, tfidf_vecs = build_tfidf_vectors(tokenized_sentences)

    # Sum tfidf scores for each sentence
    sentence_scores = []
    for i, doc_vec in enumerate(tfidf_vecs):
        sentence_scores.append((i, sum([score for _, score in doc_vec])))

    # Sort sentences by TF-IDF score
    sentence_scores = sorted(sentence_scores, key=lambda x: x[1],
                             reverse=True)

    # Return top sentences
    return [sentences[i] for i, _ in sentence_scores[:num_sentences]]
