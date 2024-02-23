"""Vector-related functions."""

import numpy as np
from gensim.matutils import kullback_leibler


def calculate_dist_matrix(lst_vecs, distance_func):
    """Calculate distance matrix for a list of vectors."""
    num_vecs = len(lst_vecs)
    dists_matrix = np.zeros((num_vecs, num_vecs))

    for i in range(num_vecs):
        for j in range(i+1, num_vecs):
            dists_matrix[i, j] = distance_func(lst_vecs[i], lst_vecs[j])
            dists_matrix[j, i] = dists_matrix[i, j]
    return dists_matrix


def calculate_avg_distance_every_vec(lst_vecs, distance_func):
    """Calculate average distance of each vector."""
    num_vecs = len(lst_vecs)
    dist_matrix = calculate_dist_matrix(lst_vecs, distance_func)
    avg_dists = dist_matrix.sum(axis=1) / (num_vecs - 1)
    return avg_dists


def cosine_similarity(a, b):
    """Compute the cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def calculate_jensen_shannon_div(vec1, vec2):
    """
    Calculate the Jensen-Shannon divergence between two vectors.

    The vectors have to sum to 1---i.e., the vectors must represent
    probability distributions.

    The Jensen-Shannon Divergence (JSD) is the average of two
    Kullback-Leibler Divergences (KL). But unlike KL, JSD is symmetric
    and bounded between 0 and 1. JS represents a type of average
    'information gain' of one distribution over the other.
    """
    # Calculate the average of the two vectors
    m = 0.5 * (vec1 + vec2)

    # Calculate Jensen-Shannon divergence
    return 0.5 * (kullback_leibler(vec1, m) +
                  kullback_leibler(vec2, m))


# def convert_to_gensim_sparse(lst_vecs):
#     """Convert a list of vectors to gensim sparse vectors."""
#     return [matutils.full2sparse(v) for v in lst_vecs]


# def convert_to_gensim_full(lst_vecs):
#     """Convert a list of vectors to gensim full vectors."""
#     length = len(lst_vecs[0])
#     return [matutils.sparse2full(v, length)
#             for v in lst_vecs]
