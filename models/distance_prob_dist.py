"""Functions for calculating similarity between probability distributions."""

from gensim.matutils import kullback_leibler


def calculate_jensen_shannon_div(vec1, vec2):
    """
    Calculate the Jensen-Shannon divergence between two vectors.

    The Jensen-Shannon Divergence (JS) is the average of two
    Kullback-Leibler Divergences (KL). But unlike KL, JS is symmetric and
    bounded between 0 and 1. JS represents a type of average
    'information gain' of one distribution over the other.
    """
    # Calculate the average of the two vectors
    m = 0.5 * (vec1 + vec2)

    # Calculate Jensen-Shannon divergence
    return 0.5 * (kullback_leibler(vec1, m) +
                  kullback_leibler(vec2, m))
