"""Search for reasonable hyperparameters in a topic model."""

import json
import random
from itertools import product

from gensim.models.coherencemodel import CoherenceModel
from gensim.models.nmf import Nmf


class ScoreHyperNMF:
    def __init__(self, ids, corpus_tk, corpus_vecs, hyperspace):
        self.ids = ids
        self.corpus_tk = corpus_tk
        self.corpus_vecs = corpus_vecs
        self.hyperspace: dict[str, list] = hyperspace

    def _sample_hyperparams(self, sample_size: int | None) -> list[dict]:
        """Select a sample of the hyperparameter space."""
        keys = self.hyperspace.keys()
        combinations = list(product(*self.hyperspace.values()))
        num_combinations = len(combinations)

        if sample_size is None or sample_size >= num_combinations:
            print(f"Returning all {num_combinations} combinations.")
            return [dict(zip(keys, param)) for param in combinations]

        sample = random.sample(combinations, sample_size)
        return [dict(zip(keys, param)) for param in sample]

    def _get_nmf_topics_sans_prob(self, nmf_model):
        """
        Return NMF topics without their probabilities.

        This functions' output is needed to calculate coherence.
        """
        num_topics = nmf_model.num_topics
        nmf_topics = []
        for topic_id in range(num_topics):
            topic = nmf_model.show_topic(topic_id)
            topic_words = [word for word, _ in topic]
            nmf_topics.append(topic_words)

        return nmf_topics

    def compute_coherence(self, nmf_model):
        """
        Compute the coherence of a topic model using c_v and u_mass.

        While c_v favors topics that are distinct but maybe not very specific,
        u_mass favors topics that are tightly focused but possibly overlapping.

        Sliding window methods (e.g., 'c_v') do not require the corpus but they
        require tokenized texts. 'u_mass' requires a corpus but not tokenized
        texts. However, Gensim uses the dictionary and the tokenized docs to
        generate the vectorized corpus if it is not provided. Information about
        whether the topic model was trained using word frequency or TF-IDF weights
        is not used to calculate the coherence scores.
        """
        topics = self._get_nmf_topics_sans_prob(nmf_model)

        kwargs = {
            "topics": topics,
            "texts": self.corpus_tk,
            "dictionary": self.ids,
        }

        cv = CoherenceModel(**kwargs, coherence="c_v")
        umass = CoherenceModel(**kwargs, coherence="u_mass")

        return {"c_v": cv.get_coherence(), "u_mass": umass.get_coherence()}

    def score_hyper(
        self, sample_size: int | None = None, write_to: str | None = None
    ) -> list[dict]:
        scores = []
        hyper_sample = self._sample_hyperparams(sample_size)
        for sample in hyper_sample:
            nmf_model = Nmf(corpus=self.corpus_vecs, id2word=self.ids, **sample)
            dct_out = {**sample, **self.compute_coherence(nmf_model)}
            if write_to:
                with open(write_to, "a") as f:
                    f.write(json.dumps(dct_out) + "\n")  # Use jsonl format
            scores.append(dct_out)
        return scores
