"""Functions for computing distances between vectors."""

from gensim.matutils import cossim


def cosine_distance(vec1, vec2):
    """Convert cosine similarity to a distance measure."""
    return 1 - cossim(vec1, vec2)
