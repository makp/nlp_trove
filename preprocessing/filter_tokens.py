"""Filter tokens."""

from vectorization.sparse_vectorization import build_tfidf_vectors


class FilterTokens:
    """Class for filtering tokens."""

    def __init__(self, min_length=2, max_length=20):
        """Initialize the FilterTokens class."""
        self.custom_stopwords = {
            'account',
            'aim',
            'also',
            'book',
            'chapter',
            'department',
            'university',
            'school',
            'email',
            'essay',
            'scientist',
            'referee',
            'et',
            'al',
            'examine',
            'important',
            'could',
            'may',
            'might',
            'paper',
            'press',
            'review',
            'used',
            'would'}
        self.content_pos = {'NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV'}
        self.noun_pos = {'NOUN', 'PROPN'}
        self.min_length = min_length
        self.max_length = max_length

    def add_custom_stopwords(self, stopwords):
        """Add custom stopwords."""
        self.custom_stopwords.update(stopwords)

    def preprocess_tokens(self, doc, remove_stop=True):
        """
        Preprocess a spaCy Doc or a list of spaCy Tokens.

        The motivation for removing long tokens is that they could be
        artifacts of malformed data. And single character tokens are
        unlikely to be useful for downstream NLP tasks.
        """
        tokens = [token.lemma_.lower() for token in doc if
                  token.is_alpha and
                  (not remove_stop or
                   (not token.is_stop and
                    token.lemma_.lower() not in self.custom_stopwords)) and
                  self.min_length <= len(token.lemma_) <= self.max_length
                  ]
        return tokens

    def keep_tokens_with_pos(self, doc, pos_tags):
        """Keep tokens with certain POS tags."""
        return [t for t in doc if t.pos_ in pos_tags]

    def drop_tokens_with_pos(self, doc, pos_tags):
        """Drop tokens with certain POS tags."""
        return [t for t in doc if t.pos_ not in pos_tags]

    def keep_tokens_with_ner(self, doc, ner_labels):
        """Keep tokens with certain NER labels."""
        return [t for t in doc if t.ent_type_ in ner_labels]

    def drop_tokens_with_ner(self, doc, ner_labels):
        """Drop tokens with certain NER labels."""
        return [t for t in doc if t.ent_type_ not in ner_labels]

    def __call__(self, doc):
        """Preprocess a spaCy Doc based on the class default arguments."""
        return self.preprocess_tokens(doc)


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
