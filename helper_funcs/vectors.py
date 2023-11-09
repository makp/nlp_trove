"""Vector-related functions."""

import numpy as np
from gensim import matutils


def calculate_avg_distance_every_vec(lst_vecs, distance_func):
    """Calculate average distance of each vector."""
    num_vecs = len(lst_vecs)
    dists_matrix = np.zeros((num_vecs, num_vecs))

    for i in range(num_vecs):
        for j in range(i+1, num_vecs):
            dists_matrix[i, j] = distance_func(lst_vecs[i], lst_vecs[j])
            dists_matrix[j, i] = dists_matrix[i, j]
    avg_dists = dists_matrix.sum(axis=1) / (num_vecs - 1)
    return avg_dists


def convert_to_gensim_sparse(lst_vecs):
    """Convert a list of vectors to gensim sparse vectors."""
    return [matutils.full2sparse(v) for v in lst_vecs]


def convert_to_gensim_full(lst_vecs):
    """Convert a list of vectors to gensim full vectors."""
    length = len(lst_vecs[0])
    return [matutils.sparse2full(v, length)
            for v in lst_vecs]
