"""Return the NMF topics of a document based on their consensus."""

import statistics
from collections import Counter

from ..helper_funcs.vectors import cosine_similarity


class DocTopics:
    def __init__(self, model):
        self.model = model

    def _run_model_on_doc(
        self,
        doc_vecs: list[tuple[int, float]],
        num_runs: int,
    ) -> dict[int, dict[int, float]]:
        """Run the model on a document `num_runs` times."""
        return {
            run: dict(self.model.get_document_topics(doc_vecs, normalize=True))
            for run in range(num_runs)
        }

    def _extract_topic_ids(
        self,
        topic_distr: dict[int, float],
        threshold: float,
    ) -> list[int]:
        """Extract topics from a topic distribution above a threshold."""
        return [topic_id for topic_id, prob in topic_distr.items() if prob > threshold]

    def calculate_consensus_per_topicid(
        self,
        topic_ids: list[list[int]],
    ) -> dict[int, float]:
        """Calculate the consensus per topic id."""
        num_runs = len(topic_ids)
        counts = Counter([topic_id for sublist in topic_ids for topic_id in sublist])
        scores = {topicid: count / num_runs for topicid, count in counts.items()}
        return dict(sorted(scores.items()))

    def select_run_based_on_consensus(
        self,
        doc_vecs: list[tuple[int, float]],
        num_runs: int = 10,
        threshold: float = 0.1,
    ) -> dict[int, float]:
        """
        Select the best run based on the consensus of topic distributions.

        This method prioritizes topics that appear frequently across multiple
        runs. However, this method is sensitive to outliers, and it might favor
        runs with topics that barely passed the threshold (0.9 and threshold +
        delta has the same influence). Further, it depends on the choice of
        threshold. Finally, this method only takes into account
        presence/absence in relation to the threshold.
        """
        # Store the topic distribution for each run
        run2distr = self._run_model_on_doc(doc_vecs, num_runs)

        # Extract the topics for each run after removing the ones with low
        # probability
        run2topics = {
            run: self._extract_topic_ids(topic_distr, threshold)
            for run, topic_distr in run2distr.items()
        }

        # Calculate the "degree of consensus" for each topic
        topic2score = self.calculate_consensus_per_topicid(list(run2topics.values()))

        # Calculate the scores for each topic distribution
        consensus_scores = dict()
        for run, topics in run2topics.items():
            score = 0
            for topicid in topics:
                score += topic2score.get(topicid, 0)
            consensus_scores[run] = score

        # Return the run with the highest score
        top_run = max(
            consensus_scores.items(),
            key=lambda x: float(x[1]) if x[1] is not None else float("-inf"),
        )[0]

        # Get the top run
        return run2distr[top_run]

    def select_median_run(
        self,
        doc_vecs: list[tuple[int, float]],
        num_runs: int = 10,
    ) -> dict[int, float]:
        """
        Select the best run based on the median of topic probabilities across
        runs.

        It robust to outliers and it doesn't rely on a threshold. But it
        produces a synthetic distribution.
        """
        # Run the model multiple times
        run2distr = self._run_model_on_doc(doc_vecs, num_runs)

        # Collect probabilities for each topic across runs
        topic_probs = {}
        for distr in run2distr.values():
            for topic_id, prob in distr.items():
                topic_probs.setdefault(topic_id, []).append(prob)

        # Compute the median probability for each topic
        median_distr = {
            topic_id: statistics.median(probs)
            for topic_id, probs in topic_probs.items()
        }
        return median_distr

    def select_run_based_on_cosine_dist(
        self,
        doc_vecs: list[tuple[int, float]],
        num_runs: int = 10,
    ) -> dict[int, float]:
        """
        Select the best run based on the cosine similarity to a consensus vector.

        It considers the overall distribution of topics across all runs. But
        cosine similarity emphasizes direction over maginitude.
        """
        # Run the model multiple times
        run2distr = self._run_model_on_doc(doc_vecs, num_runs)
        # Build a sorted list of all topic IDs present across runs
        all_topics = sorted(
            {topic_id for distr in run2distr.values() for topic_id in distr}
        )
        # Compute a consensus vector using the average probabilities
        consensus_vector = [
            sum(distr.get(topic, 0) for distr in run2distr.values()) / num_runs
            for topic in all_topics
        ]
        # Select the run whose topic distribution is closest to the consensus vector based on cosine similarity
        best_run = None  # Initialize with default value
        best_similarity = float("-inf")
        for run, distr in run2distr.items():
            run_vector = [distr.get(topic, 0) for topic in all_topics]
            sim = cosine_similarity(run_vector, consensus_vector)
            if sim > best_similarity:
                best_similarity = sim
                best_run = run
        if best_run is None:
            return {}
        else:
            return run2distr[best_run]
