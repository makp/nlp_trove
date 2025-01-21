"""Transform text into sparse vectors using Gensim."""

from gensim.corpora import Dictionary
from gensim.models import TfidfModel


class SparseVec:
    def __init__(self, docs):
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

        BoW vectors are tuples of token IDs and their counts.
        """
        return [self.tk_id_map.doc2bow(doc) for doc in self.docs]

    def build_tfidf_vectors(self):
        """
        Build TF-IDF vectors from tokenized documents.

        The returned vectors are tuples of token IDs and TF-IDF weights.
        """
        bow_vecs = self.build_bow_vectors()
        tfidf = TfidfModel(bow_vecs)
        return [tfidf[vec] for vec in bow_vecs]
