from gensim.models.nmf import Nmf


class WriteTopics:
    """Write topics from an NMF model to a markdown file for inspection."""

    def __init__(self, model: Nmf):
        self.model = model

    def _get_topics(self, num_words: int) -> list[tuple]:
        """Get topics from an NMF model."""
        return self.model.show_topics(
            num_words=num_words,  # return more words
            num_topics=-1,  # return all topics
            formatted=False,  # return (word, prob) tuples
            normalize=True,  # normalize probs
        )

    def write_nmf_topics_to_file(
        self,
        filepath: str,
        num_words: int = 500,
        metadata: None | dict = None,
    ) -> None:
        """Write NMF topics and its metadata to a markdown."""

        nmf_topics = dict(self._get_topics(num_words))

        with open(filepath, "w") as f:
            if metadata:
                # Add YAML metadata
                f.write("---\n")
                for k, v in metadata.items():
                    f.write(f"{k}: {v}\n")
                f.write("---\n\n\n")

            f.write("# NMF Topic Model Results\n\n")
            for topic_id, words_weights in nmf_topics.items():
                # Write topic header
                f.write(f"## Topic {topic_id}\n\n")

                # Write table header
                f.write("| Word | Weight |\n")
                f.write("|------|--------|\n")

                # Write word-weight pairs as table rows
                for word, weight in words_weights:
                    f.write(f"| {word} | {weight:.4f} |\n")
                f.write("\n")
