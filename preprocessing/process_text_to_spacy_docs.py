"""Preprocess text data to spaCy docs."""

import spacy
from spacy.tokens import DocBin


class TextPreprocessor:
    """Preprocess text data to spaCy docs."""

    def __init__(self,
                 model="en_core_web_trf",
                 disable_pipes=None,
                 batch_size=50):
        """Initialize the class."""
        self.nlp = spacy.load(model, disable=disable_pipes or [])
        self.batch_size = batch_size

    def process_texts(self, texts):
        """Process texts in batches."""
        text_stream = (text for text in texts)
        for doc in self.nlp.pipe(text_stream,
                                 batch_size=self.batch_size):
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
