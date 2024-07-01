"""Transform text data to spaCy Docs."""

import pandas as pd
import spacy
from spacy.tokens import DocBin


class TextToDocs:
    """Transform plain text data to spaCy Doc objects."""

    # Confirm GPU availability
    print("GPU available:", spacy.prefer_gpu())  # type: ignore

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

    def process_texts(self, series):
        """Process a Pandas Series and return a generator of spaCy Doc objects along with indices."""
        for idx, doc in zip(
            series.index, self.nlp.pipe(series, batch_size=self.batch_size)
        ):
            yield idx, doc

    def serialize_docs(self, docs_with_idxs, output_path):
        """Serialize docs."""
        doc_bin = DocBin()
        doc_meta = []
        for idx, doc in docs_with_idxs:
            doc_bin.add(doc)
            doc_meta.append(idx)
        doc_bin.to_disk(output_path)
        with open(output_path + "_meta.txt", "w") as meta_file:
            for index in doc_meta:
                meta_file.write(f"{index}\n")

    def load_serialized_docs(self, filepath):
        """Load serialized docs and return a Pandas Series of spaCy Doc objects."""
        doc_bin = DocBin().from_disk(filepath)
        with open(filepath + "_meta.txt", "r") as meta_file:
            idxs = [line.strip() for line in meta_file]
        docs = list(doc_bin.get_docs(self.nlp.vocab))
        return pd.Series(data=docs, index=idxs)
