"""Transform text data to spaCy Docs."""

import gc
import logging
import os
import subprocess
from collections import Counter

import pandas as pd
import psutil
import spacy
from spacy.tokens import Doc, DocBin

# Confirm GPU availability
# NOTE: `prefer_gpu` has to be loaded *before* any pipelines
print("GPU available? ", spacy.prefer_gpu())  # type: ignore


def analyze_memory_usage():
    """Analyze memory usage by counting number of objects in memory."""
    type_count = Counter(type(o).__name__ for o in gc.get_objects())
    return type_count


class SeriesToDocs:
    """Transform text Series to spaCy Doc objects."""

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
        n_process=1,
        mem_log=False,
    ):
        """Initialize the class."""
        self.nlp = spacy.load(model, disable=disable_pipes or [])
        if enable_pipe:
            self.nlp.add_pipe(enable_pipe)
        self.batch_size = batch_size
        self.n_process = n_process
        if not Doc.has_extension("idx"):
            Doc.set_extension("idx", default=None)
        self.mem_log = mem_log
        if mem_log:
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)
            logging.basicConfig(
                filename=os.path.join(log_dir, "memory_usage.log"),
                level=logging.INFO,
                format="%(asctime)s - %(message)s",
            )
            logging.info("Memory usage log")

    def stream_text_series_as_docs(self, series):
        """Stream text series data as spaCy Doc objects."""
        doc_stream = ((text, {"idx": str(idx)}) for idx, text in series.items())
        for doc, context in self.nlp.pipe(
            doc_stream,
            batch_size=self.batch_size,
            as_tuples=True,
            n_process=self.n_process,
        ):
            doc._.idx = context["idx"]
            yield doc

    def convert_text_series_to_docs_and_serialize(self, series):
        """
        Convert a Series of texts to spaCy Doc objects and serialize them.

        Although Doc objects have a `to_bytes` method that serializes the Doc
        object to a binary format, the `DocBin` class is more efficient for
        serializing multiple `Doc` objects. Source:
        <https://spacy.io/usage/saving-loading#docs>
        """
        # Create a DocBin object
        # NOTE: `store_user_data` is set to True to store the extension data
        doc_bin = DocBin(store_user_data=True)
        for doc in self.stream_text_series_as_docs(series):
            doc_bin.add(doc)
            if self.mem_log:
                gc.collect()  # Force garbage collection before counting objects
                num_objs = len(gc.get_objects())
                # psutil
                process = psutil.Process()
                logging.info(
                    f"Number of Docs in DocBin: {len(doc_bin)};\n"
                    f"Number of objects tracked by gc: {num_objs};\n"
                    f"Object counts: {dict(analyze_memory_usage().most_common(10))}\n"
                    f"Total memory usage in MB: {process.memory_info().rss / (1024 * 1024):.2f}\n"
                    "---------------------------------------------"
                )

        return doc_bin.to_bytes()

    def deserialize_docs(self, bytes_data):
        """Deserialize Doc objects and return them as a list."""
        doc_bin = DocBin().from_bytes(bytes_data)
        return list(doc_bin.get_docs(self.nlp.vocab))

    def deserialize_docs_as_series(self, bytes_data):
        """Deserialize Doc objects and return them as a Pandas Series."""
        docs = self.deserialize_docs(bytes_data)
        return pd.Series({doc._.idx: doc for doc in docs})


class TextToDocs:
    """Transform plain text to spaCy Doc objects."""

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

    def convert_text_to_docs_and_serialize(self, text):
        """Convert texts to spaCy Doc objects and serialize them."""
        doc_bin = DocBin()
        for doc in self.nlp.pipe(text, batch_size=self.batch_size):
            doc_bin.add(doc)
        return doc_bin.to_bytes()

    def deserialize_docs(self, bytes_data):
        """Deserialize Doc objects and return them as a list."""
        doc_bin = DocBin().from_bytes(bytes_data)
        return list(doc_bin.get_docs(self.nlp.vocab))
