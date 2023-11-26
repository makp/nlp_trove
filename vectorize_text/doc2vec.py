"""Train a doc2vec model."""

from gensim.models.doc2vec import Doc2Vec, TaggedDocument


class TaggedDocumentGenerator:
    """
    Build a generator of tagged documents.

    Gensim requires data in the form of `TaggedDocument` objects,
    which are pairs of `words` (the tokenized text) and `tags` (unique
    identifiers for each document).
    """

    def __init__(self, tokenized_docs):
        """Initialize the TaggedDocumentGenerator."""
        self.tokenized_docs = tokenized_docs

    def __iter__(self):
        """Yield a tagged document."""
        for i, words_list in enumerate(self.tokenized_docs):
            yield TaggedDocument(words=words_list, tags=[str(i)])


def train_doc2vec_model(tokenized_docs,
                        min_count=5,
                        seed=42,
                        **keyargs):
    """Train a doc2vec model."""
    # Check if the input is valid
    if not all(isinstance(doc, (list, tuple)) and
               all(isinstance(token, str) for token in doc)
               for doc in tokenized_docs):
        raise ValueError('Each document should be a list of strings.')

    # Define the vec2doc model
    model = Doc2Vec(min_count=min_count,
                    seed=seed,
                    **keyargs)

    # Build the tagged documents
    tagged_docs = TaggedDocumentGenerator(tokenized_docs)

    # Build the vocabulary
    model.build_vocab(tagged_docs)

    # Train the model
    model.train(tagged_docs,
                total_examples=model.corpus_count,
                epochs=model.epochs)

    return model
