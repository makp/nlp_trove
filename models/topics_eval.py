"""Search for reasonable hyperparameters in a topic model."""

import inspect
import json
import random
from itertools import product

import pandas as pd
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.ldamodel import LdaModel
from gensim.models.nmf import Nmf


class EvalHyper:
    DEFAULT_SEED = {"random_state": [42]}

    def __init__(self, ids, corpus_tk, corpus_vec=None, hyperspace=None):
        self.ids = ids
        self.corpus_tk = corpus_tk
        self.corpus_vec = corpus_vec
        if hyperspace is None:
            self.hyperspace = self.DEFAULT_SEED.copy()
        else:
            if "random_state" not in hyperspace:
                print("WARNING: Adding `random_state` to hyperspace.")
                hyperspace.update(self.DEFAULT_SEED)
            self.hyperspace = hyperspace

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

    def _get_nmf_topics_sans_prob(self, model):
        """
        Return NMF topics without their probabilities.

        This function is needed to calculate coherence for NMF models.
        """
        num_topics = model.num_topics
        lst_topics = []
        for topic_id in range(num_topics):
            topic = model.show_topic(topicid=topic_id, topn=100000, normalize=True)
            topic_words = [word for word, _ in topic]
            lst_topics.append(topic_words)

        return lst_topics

    def compute_coherence(self, model):
        """
        Compute the coherence of a topic model using c_v and u_mass.

        While the dictionary (token to ID mapping) is required for calculating
        coherence scores, the coherence scores differ in whether they need the
        (vectorized) corpus or the tokenized texts. Sliding window methods
        (e.g., 'c_v') do not require the vectorized corpus but require
        tokenized texts---info about the token order is needed to define the
        sliding windows. 'u_mass' requires a vectorized corpus but not
        tokenized texts. Information about the token order is not needed
        because 'u_mass' uses the whole document as its context window.
        However, if the vectorized corpus is not provided, Gensim can still
        calculate the 'u_mass' by using the dictionary and the tokenized docs
        to vectorize the documents.


        Information about whether the topic model was trained using word
        frequency or TF-IDF weights is not used to calculate the coherence
        scores. Coherence scores solely rely on the word co-occurrence stats
        and the topic-word lists.
        """

        kwargs = {
            "texts": self.corpus_tk,
            "dictionary": self.ids,
        }

        if isinstance(model, LdaModel):
            kwargs.update({"model": model})
        elif isinstance(model, Nmf):
            topics = self._get_nmf_topics_sans_prob(model)
            kwargs.update({"topics": topics})

        cv = CoherenceModel(**kwargs, coherence="c_v")
        umass = CoherenceModel(**kwargs, coherence="u_mass")

        return {"c_v": cv.get_coherence(), "u_mass": umass.get_coherence()}

    def _return_default_params(self, function):
        signature = inspect.signature(function.__init__)
        pars_to_exclude = ("self", "corpus", "id2word")
        return {
            k: v.default
            for k, v in signature.parameters.items()
            if v.default is not inspect.Parameter.empty and k not in pars_to_exclude
        }

    def train_model(self, model_type, **kwargs):
        """Train a topic model (NMF or LDA)."""
        func_map = {
            "nmf": Nmf,
            "lda": LdaModel,
        }

        training_func = func_map[model_type]

        model = training_func(
            corpus=self.corpus_vec,
            id2word=self.ids,
            **kwargs,
        )

        params = {**self._return_default_params(training_func), **kwargs}

        return model, params

    def score_hyper_single(
        self,
        pipe_name: str,
        params: dict,
        model_type: str = "nmf",
        write_to: str | None = None,
    ):
        model, all_params = self.train_model(model_type, **params)
        score = {
            "pipeline": pipe_name,
            **all_params,
            **self.compute_coherence(model),
        }
        if write_to:
            with open(write_to, "a") as f:
                f.write(json.dumps(score) + "\n")  # Use jsonl format
        return score

    def score_hyper(
        self,
        pipe_name: str,
        sample_size: int | None = None,
        model_type: str = "nmf",
        write_to: str | None = None,
    ) -> list[dict]:
        """Calculate `c_v` and `u_mass` for a sample of the hyperparameters."""
        scores = []
        hyper_sample = self._sample_hyperparams(sample_size)
        for sample in hyper_sample:
            single_score = self.score_hyper_single(
                pipe_name=pipe_name,
                params=sample,
                model_type=model_type,
                write_to=write_to,
            )
            scores.append(single_score)
        return scores


class ProcessScores:
    def __init__(self, path: str):
        self.path = path

    def read_scores(self) -> pd.DataFrame:
        """Read the scores from a file as a DataFrame."""
        with open(self.path, "r") as f:
            data = [json.loads(line) for line in f]
        return pd.DataFrame(data)

    def normalize_scores(self, scores: pd.Series) -> pd.Series:
        """Normalize the scores."""
        return (scores - scores.min()) / (scores.max() - scores.min())

    def combine_scores(
        self,
        scores,
        weight=0.5,
        columns=("c_v", "u_mass"),
    ):
        """Combine two scores using a weighted average."""
        cv_normalized, umass_normalized = (
            self.normalize_scores(scores[columns[0]]),
            self.normalize_scores(scores[columns[1]]),
        )
        return (weight * cv_normalized) + (1 - weight) * umass_normalized


# NOTE: Misc functions for topic modeling that need to be reviewed
#
# def list_topics_for_bow_sorted(lda_model, bow):
#     """
#     Return the list of topics for a bow vector.
#
#     The list is sorted by the probability of each topic.
#     """
#     topic_dist = lda_model.get_document_topics(bow, minimum_probability=None)
#     return sorted(topic_dist, key=lambda x: x[1], reverse=True)
#
#
# def get_top_n_docs_for_topic(series_bow, lda_model, topic_id, num_docs=1):
#     """Get the indexes of the top `num_docs` documents for a given topic."""
#     lst = []
#     for idx, bow in series_bow.items():
#         topic_dist = dict(lda_model.get_document_topics(bow))
#         prob = topic_dist.get(topic_id, 0)
#         lst.append((idx, prob))
#     lst.sort(key=lambda x: x[1], reverse=True)
#     return lst[:num_docs]
#

# def compute_perplexity(lda_model, test_corpus):
#     """
#     Compute and return the perplexity of a LDA model for a holdout
#     corpus.
#     Perplexity measures how well a probability model predicts a
#     sample. The lower the score, the better.
#     """
#     num_docs = len(test_corpus)
#     unnormalized_log_perplexity = 0
#     for doc_bow in test_corpus:
#         doc_topics = lda_model.get_document_topics(doc_bow,
#                                                    minimum_probability=0)
#         doc_probs = [prob for (_, prob) in doc_topics]
#         doc_perplexity = -np.dot(np.log(doc_probs), doc_probs)
#         unnormalized_log_perplexity += doc_perplexity
#     normalized_log_perplexity = unnormalized_log_perplexity / num_docs
#     perplexity = np.exp(normalized_log_perplexity)

#     return perplexity
