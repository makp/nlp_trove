"""Functions for clustering and clustering evaluation."""

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np


def evaluate_kmeans_clusters(vecs, n_clusters):
    """Calculate silhouette score and variance of cluster sizes."""
    # Generate kmeans clusters
    kmeans = KMeans(n_clusters=n_clusters,
                    algorithm='elkan',  # dense data
                    n_init=10,
                    random_state=42)
    kmeans.fit(vecs)

    # Calculate silhouette score
    sil_score = silhouette_score(vecs, kmeans.labels_)

    # Calculate variance of cluster sizes
    cluster_sizes = np.bincount(kmeans.labels_)
    var = np.var(cluster_sizes)

    return [sil_score, var]
