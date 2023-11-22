"""Functions for clustering and clustering evaluation."""

from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
from collections import Counter
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


def apply_dbscan(vecs, eps=0.5, min_samples=5):
    """
    Apply DBSCAN clustering to the vectors.

    Notes about the parameters:
    - The `eps` parameter defines the radius of neighborhood around a
      point. A small `eps` can divide the data in many small clusters.
    - The `min_samples` parameter reflects the minimum number of
      samples in a nb for a point to be considered a core point,
      including the point itself. A larger `min_samples` will result
      in a greater density to form a cluster.
    """
    # Generate DBSCAN clusters
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    clusters = dbscan.fit_predict(vecs)

    # Count the number of vectors in each cluster
    cluster_counts = Counter(clusters)

    # Find indices of outliers
    noise_indices = np.where(clusters == -1)[0]

    return clusters, cluster_counts, noise_indices
