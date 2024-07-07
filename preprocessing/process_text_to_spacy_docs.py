"""Transform text data to spaCy Docs."""

import subprocess

import spacy
from spacy.tokens import DocBin


class TextToDocs:
    """Transform plain text data to spaCy Doc objects."""

    @staticmethod
    def validate_spacy():
        """Validate spaCy installation and GPU availability."""
        # Validate spaCy installation
        result = subprocess.run(
            ["python", "-m", "spacy", "validate"], capture_output=True, text=True
        )
        print("Check installed pipelines: ", result.stdout)
        # Confirm GPU availability
        print("GPU available? ", spacy.prefer_gpu())  # type: ignore

    def __init__(
        self,
        model="en_core_web_trf",
        disable_pipes=None,
        enable_pipe=None,
        batch_size=25,
    ):
        """Initialize the class."""
        self.nlp = spacy.load(model, disable=disable_pipes or [])
        if enable_pipe:
            self.nlp.add_pipe(enable_pipe)
        self.batch_size = batch_size

    def convert_text_series_to_docs_as_gen(self, series):
        """Return a generator of spaCy Doc objects along with their indices
        from texts stored as Pandas Series."""
        for idx, doc in zip(
            series.index, self.nlp.pipe(series, batch_size=self.batch_size)
        ):
            yield idx, doc

    def convert_text_series_to_docs_and_serialize(self, series):
        """
        Convert a Series of texts to spaCy Doc objects and serialize them.

        Doc objects have a to_bytes() method that serializes the Doc object to a binary format. However, the DocBin class is more efficient for serializing multiple Doc objects. See <https://spacy.io/usage/saving-loading>.
        """
        doc_bin = DocBin()
        doc_meta = []
        docs_with_idxs = self.convert_text_series_to_docs_as_gen(series)
        for idx, doc in docs_with_idxs:
            doc_bin.add(doc)
            doc_meta.append(idx)
        data = doc_bin.to_bytes()
        return (doc_meta, data)

    def deserialize_docs(self, bytes_data):
        """Deserialize Doc objects and return them as a list."""
        doc_bin = DocBin().from_bytes(bytes_data)
        return list(doc_bin.get_docs(self.nlp.vocab))
