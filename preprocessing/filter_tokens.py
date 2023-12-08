"""Filter tokens."""

from vectorization.sparse_vectorization import build_tfidf_vectors


class FilterTokens:
    """Class for filtering tokens."""

    def __init__(self):
        """Initialize the FilterTokens class."""
        self.custom_stopwords = set('would could may might account et al used also'.split(' ')) # noqa
        self.content_pos = {'NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV'}
        self.noun_pos = {'NOUN', 'PROPN'}

    def remove_custom_stopwords(self, tokens):
        """Remove stopwords from the given list of tokens."""
        return [t for t in tokens if t not in self.custom_stopwords]

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

    def preprocess_tokens(self, doc):
        """Preprocess the given spaCy doc."""
        tokens = [token.lemma_ for token in doc if
                  token.is_alpha and
                  not token.is_punct and  # redundant?
                  not token.is_stop]
        tokens = self.remove_custom_stopwords(tokens)
        tokens = self.remove_short_and_long_tokens(tokens)
        return tokens

    def filter_doc_with_pos(self, doc, pos_tags):
        """Filter tokens based on spaCy POS tags."""
        tokens = [t for t in doc if t.pos_ in pos_tags]
        return self.preprocess_tokens(tokens)


class FilterTokensWithTFIDF:
    """Filter tokens based on their TF-IDF scores."""

    def __init__(self, tokenized_docs, threshold=0.1):
        """Initialize the FilterTokensWithTFIDF class."""
        self.tokenized_docs = tokenized_docs
        self.dictionary, self.tfidf_vecs = build_tfidf_vectors(
            tokenized_docs)
        self.threshold = threshold
        self.tokens_to_keep = self.get_tokens_above_tfidf_score()

    def get_tokens_above_tfidf_score(self):
        """Return tokens above a certain TF-IDF score."""
        tokens_to_keep = set()
        for doc_vec in self.tfidf_vecs:
            for token_id, score in doc_vec:
                if score > self.threshold:
                    tokens_to_keep.add(self.dictionary[token_id])
        return tokens_to_keep

    def filter_doc(self, tokenized_doc):
        """Filter tokens based on a list of tokens to keep."""
        return [token for token in tokenized_doc
                if token in self.tokens_to_keep]
