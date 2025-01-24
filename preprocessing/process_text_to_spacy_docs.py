"""Transform text data to spaCy Docs."""

import logging
import os
import pickle
import subprocess
import tracemalloc
from collections.abc import Generator, Hashable

import pandas as pd
import psutil
import spacy
from spacy.tokens import Doc, DocBin

# Confirm GPU availability
# NOTE: `prefer_gpu` has to be loaded *before* any pipelines
print("GPU available? ", spacy.prefer_gpu())  # type: ignore


class SeriesToDocs:
    """Transform Series storing text to spaCy Doc objects."""

    @staticmethod
    def validate_spacy():
        """Validate spaCy installation."""
        result = subprocess.run(
            ["python", "-m", "spacy", "validate"], capture_output=True, text=True
        )
        print("Check installed pipelines: ", result.stdout)

    def __init__(
        self,
        model: str | None = "en_core_web_trf",
        disable_pipes=None,
        enable_pipe=None,
        batch_size=25,
        n_process=1,
        mem_log=False,
    ):
        """Initialize spaCy pipeline and parameters."""
        self.nlp = (
            spacy.blank("en")
            if model is None
            else spacy.load(model, disable=disable_pipes or [])
        )
        if enable_pipe:
            self.nlp.add_pipe(enable_pipe)
        self.batch_size = batch_size
        self.n_process = n_process
        self.mem_log = mem_log
        if mem_log:
            self._setup_logging()

    def _setup_logging(self):
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            filename=os.path.join(log_dir, "memory_usage.log"),
            level=logging.INFO,
            format="%(asctime)s - %(message)s",
        )
        logging.info("Memory usage log during serialization")

    def _stream_docs(self, series: pd.Series) -> Generator[tuple[Hashable, Doc]]:
        """Stream Series containing text data as spaCy Doc objects."""
        # Format Series in a way that spaCy can process
        text_tuples = [(text, {"idx": idx}) for idx, text in series.items()]

        for doc, context in self.nlp.pipe(
            text_tuples,
            batch_size=self.batch_size,
            n_process=self.n_process,
            as_tuples=True,
        ):
            yield context["idx"], doc

    def convert_series_to_docs(
        self, series: pd.Series
    ) -> tuple[list[Hashable], DocBin]:
        """
        Convert a Series containing texts to spaCy Doc, and bundle them in a
        DocBin.

        The `DocBin` class is more efficient for storing multiple `Doc`
        objects. Source: <https://spacy.io/usage/saving-loading#docs>
        """
        if self.mem_log:
            tracemalloc.start()
            snapshot1 = tracemalloc.take_snapshot()

        # Create a `DocBin` to store the `Doc` objects
        doc_bin = DocBin()

        # Convert texts to Docs
        idx_list = []
        count = 0
        for idx, doc in self._stream_docs(series):
            doc_bin.add(doc)
            idx_list.append(idx)

            # Log memory usage once every batch
            count += 1
            if self.mem_log and count % self.batch_size == 0:
                self._log_memory_usage(doc_bin, snapshot1)  # type: ignore

        if self.mem_log:
            tracemalloc.stop()

        assert len(idx_list) == len(doc_bin)

        return idx_list, doc_bin

    def convert_series_to_docs_and_serialize(
        self, series: pd.Series, path_idx: str, path_docbin: str
    ) -> None:
        """Convert a Series of texts to spaCy Doc objects and serialize them."""
        idx_list, doc_bin = self.convert_series_to_docs(series)
        doc_bin.to_disk(path_docbin)
        print(f"Serialized DocBin to {path_docbin}")
        with open(path_idx, "wb") as f:
            pickle.dump(idx_list, f)
        print(f"Serialized index list to {path_idx}")

    def _log_memory_usage(self, object_name, snapshot_base):
        process = psutil.Process()
        snapshot2 = tracemalloc.take_snapshot()
        top_stats = snapshot2.compare_to(snapshot_base, "lineno")  # type: ignore
        logging.info(
            f"Object length ({type(object_name)}): {len(object_name)};\n"
            f"Total memory usage in MB: {process.memory_info().rss / (1024**2):.2f}\n"
            f"Tracemalloc top stats: {top_stats[:5]}\n"
            # current, peak = tracemalloc.get_traced_memory()
            "---------------------------------------------"
        )

    def deserialize_docbin_as_series(
        self, path_idx: str, path_docbin: str
    ) -> pd.Series:
        """Deserialize Doc objects and return them as a Pandas Series."""
        doc_bin = DocBin().from_disk(path_docbin)
        idx = pd.read_pickle(path_idx)
        return pd.Series(doc_bin.get_docs(self.nlp.vocab), index=idx)


class SeriesToDocsWithAttrib(SeriesToDocs):
    """
    Transform text Series to spaCy Doc objects with custom extension attributes.

    Further info on extension attributes:
    <https://spacy.io/usage/processing-pipelines#custom-components-attributes>

    *NOTE*: Using spaCy extension attributes to store the series index
    has dramatically increased the memory usage of this class.
    """

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
        super().__init__(
            model, disable_pipes, enable_pipe, batch_size, n_process, mem_log
        )
        if not Doc.has_extension("idx"):
            Doc.set_extension("idx", default=None)

    def stream_docs_with_attributes(self, series):
        """
        Stream text series data as spaCy Doc objects with custom attributes.

        Source: <https://spacy.io/usage/processing-pipelines#processing>
        """
        text_tuples = [(text, {"idx": str(idx)}) for idx, text in series.items()]
        for doc, context in self.nlp.pipe(
            text_tuples,
            batch_size=self.batch_size,
            n_process=self.n_process,
            as_tuples=True,
        ):
            doc._.idx = context["idx"]
            yield doc

    def serialize_docs_with_attributes(self, series):
        """
        Convert a Series of texts to spaCy Doc objects and serialize them.
        """
        if self.mem_log:
            tracemalloc.start()
            snapshot1 = tracemalloc.take_snapshot()

        # Create a DocBin object
        # `store_user_data` is set to True to store the extension data
        doc_bin = DocBin(store_user_data=True)

        # Serialize the text data

        for doc in self.stream_docs_with_attributes(series):
            doc_bin.add(doc)

            if self.mem_log:
                self._log_memory_usage(doc_bin, snapshot1)  # type: ignore

        if self.mem_log:
            tracemalloc.stop()

        return doc_bin.to_bytes()

    def deserialize_docs_with_attributes_as_series(self, bytes_data):
        """Deserialize Doc objects and return them as a Pandas Series."""
        docs = self.deserialize_docbin(bytes_data)
        return pd.Series({doc._.idx: doc for doc in docs})
