"""Transform text data to spaCy Docs."""

import subprocess

import pandas as pd
import spacy
from spacy.tokens import Doc, DocBin


class TextToDocs:
    """Transform plain text stored as Pandas Series to spaCy Doc objects."""

    # Confirm GPU availability
    print("GPU available? ", spacy.prefer_gpu())  # type: ignore

    @staticmethod
    def validate_spacy():
        """Validate spaCy installation."""
        result = subprocess.run(
            ["python", "-m", "spacy", "validate"], capture_output=True, text=True
        )
        print("Check installed pipelines: ", result.stdout)

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
        if not Doc.has_extension("idx"):
            Doc.set_extension("idx", default=None)

    def stream_text_series(self, series):
        """Stream text series data as spaCy Doc objects."""
        data = [(text, {"idx": idx}) for idx, text in series.items()]
        for doc, context in self.nlp.pipe(
            data, batch_size=self.batch_size, as_tuples=True
        ):
            doc._.idx = str(context["idx"])
            yield doc

    def convert_text_series_to_docs_and_serialize(self, series):
        """
        Convert a Series of texts to spaCy Doc objects and serialize them.

        Doc objects have a `to_bytes` method that serializes the Doc object to
        a binary format. However, the `DocBin` class is more efficient for
        serializing multiple `Doc` objects. See
        <https://spacy.io/usage/saving-loading> for further details.
        """
        # Create a DocBin object
        # NOTE: `store_user_data` is set to True to store the extension data
        doc_bin = DocBin(store_user_data=True)
        for doc in self.stream_text_series(series):
            doc_bin.add(doc)
        return doc_bin.to_bytes()

    def deserialize_docs(self, bytes_data):
        """Deserialize Doc objects and return them as a list."""
        doc_bin = DocBin().from_bytes(bytes_data)
        return list(doc_bin.get_docs(self.nlp.vocab))

    def deserialize_docs_as_series(self, bytes_data):
        """Deserialize Doc objects and return them as a Pandas Series."""
        docs = self.deserialize_docs(bytes_data)
        index = [doc._.idx for doc in docs]
        return pd.Series(data=docs, index=index)
