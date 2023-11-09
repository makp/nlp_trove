"""Vector-related functions."""

import numpy as np


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
