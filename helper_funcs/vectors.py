"""Vector-related functions."""

import numpy as np
from gensim import matutils
import pickle


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


def convert_to_gensim_sparse(lst_vecs):
    """Convert a list of vectors to gensim sparse vectors."""
    return [matutils.full2sparse(v) for v in lst_vecs]


def convert_to_gensim_full(lst_vecs):
    """Convert a list of vectors to gensim full vectors."""
    length = len(lst_vecs[0])
    return [matutils.sparse2full(v, length)
            for v in lst_vecs]


def store_sbert_embeddings(sentences, embeddings,
                           fname='sbert_embeddings.pkl'):
    """Store sentence-BERT embeddings."""
    with open(fname, "wb") as fOut:
        pickle.dump({'sentences': sentences, 'embeddings': embeddings}, fOut,
                    protocol=pickle.HIGHEST_PROTOCOL)


def load_sbert_embeddings(fname='sbert_embeddings.pkl'):
    """Load sentence-BERT embeddings."""
    with open(fname, "rb") as fIn:
        data = pickle.load(fIn)
    return data['sentences'], data['embeddings']
