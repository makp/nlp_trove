"""Return the NMF topics of a document based on their consensus."""

from collections import Counter


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
