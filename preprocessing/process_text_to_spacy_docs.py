"""Preprocess text data to spaCy docs."""

import spacy
from spacy.tokens import DocBin


class TextPreprocessor:
    """Preprocess text data to spaCy docs."""

    # Confirm GPU availability
    print("GPU available:", spacy.prefer_gpu())

    def __init__(self,
                 model="en_core_web_trf",
                 disable_pipes=None,
                 enable_pipe=None,
                 batch_size=25):
        """Initialize the class."""
        self.nlp = spacy.load(model, disable=disable_pipes or [])
        if enable_pipe:
            self.nlp.add_pipe(enable_pipe)
        self.batch_size = batch_size

    def process_texts(self, texts):
        """Return a generator of spaCy Doc objects."""
        for doc in self.nlp.pipe(
                texts, batch_size=self.batch_size):
            yield doc

    def serialize_docs(self, docs, output_path):
        """Serialize docs."""
        doc_bin = DocBin()
        for doc in docs:
            doc_bin.add(doc)
        doc_bin.to_disk(output_path)

    def load_serialized_docs(self, filepath):
        """Load serialized docs."""
        doc_bin = DocBin().from_disk(filepath)
        return list(doc_bin.get_docs(self.nlp.vocab))
