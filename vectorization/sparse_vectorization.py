"""Transform text into sparse vectors using Gensim."""

from gensim.corpora import Dictionary, MmCorpus
from gensim.models import TfidfModel


class SparseVec:
    def __init__(self, docs=None):
        if docs is not None:
            self.docs = docs
            self.tk_id_map = Dictionary(self.docs)

    def filter_tokens(self, no_below_n=1, no_above_f=1, keep_n=None):
        """
        Filter tokens and update the dictionary.

        The kwarg `no_below_n` is the number of documents and `no_above_f` is a
        fraction of the total docs. Keep `keep_n` most frequent tokens after
        the above filtering. Keep all if `None`.
        """
        self.tk_id_map.filter_extremes(
            no_below=no_below_n,
            no_above=no_above_f,
            keep_n=keep_n,  # type: ignore
        )

    def build_bow_vectors(self):
        """
        Build bag-of-words (BoW) vectors from tokenized documents.

        BoW vectors are tuples of token IDs and their counts in the document.
        """
        return [self.tk_id_map.doc2bow(doc) for doc in self.docs]

    def build_tfidf_vectors(self):
        """
        Build TF-IDF vectors from tokenized documents.

        The returned vectors are tuples of token IDs and TF-IDF weights.
        """
        tfidf = TfidfModel(dictionary=self.tk_id_map)
        bow_vecs = self.build_bow_vectors()
        return [tfidf[vec] for vec in bow_vecs]

    def serialize_vectors(self, vecs, path="sparse_vecs.mm"):
        """
        Serialize vectors to a file.

        The vectors are serialized in the Matrix Market format.
        """
        MmCorpus.serialize(path, vecs)

    def deserialize_vectors(self, path="sparse_vecs.mm"):
        """
        Deserialize vectors from a file.

        The vectors are deserialized from the Matrix Market format.
        """
        return MmCorpus(path)

    def save_dictionary(self, dictionary=None, path="sparse_vecs.dict"):
        """Save the dictionary to a file."""
        dictionary = dictionary or self.tk_id_map
        dictionary.save(path)

    def load_dictionary(self, path="sparse_vecs.dict"):
        """Load the dictionary from a file."""
        return Dictionary.load(path)
