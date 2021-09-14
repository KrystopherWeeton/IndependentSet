from typing import Set

import numpy as np

from util.new_graph.models.graph import Graph

"""
Utillity for spectral (Linear Algebra) functionality
"""

def is_symmetric(a, rtol=1e-05, atol=1e-08) -> bool:
    """
    Returns flag for whether the provided matrix is symmeric
    """
    return np.allclose(a, a.T, rtol=rtol, atol=atol)


def adjacency_matrix_eigenvector(A: np.array, t: int) -> np.array:
    """
    Returns the eigenvector corresponding to the t'th largest eigenvalue.
    Errors on non-square matrix or if `t` is too large.
    NOTE: Expects the array provided is an adjacency matrix, e.g. real symmetric
    """
    shape = A.shape
    assert len(shape) == 2, f"Array provided is not a matrix, has {len(shape)} dimensions."
    assert shape[0] == shape[1], f"Matrix provided is not square, {shape[0]} != {shape[1]}"
    assert is_symmetric(A), f"Non-symmetric matrix provided"
    w, v = np.linalg.eig(A)
    seen: Set = set()
    tuples = sorted([(w[i], v[i]) for i in range(len(w)) if w[i] not in seen and not seen.add(w[i])], key=lambda x: -x[0])
    assert len(tuples) >= t, f"Only {len(tuples)} unique eigenvalues. Cannot access the {t}'th"
    return tuples[t][1]


def power_iteration(A, iterations: int) -> np.array:
    """
    Compute the principal eigenvector of A through power_iteration method
    (https://en.wikipedia.org/wiki/Power_iteration)
    """
    b_k = np.random.rand(A.shape[1])
    for _ in range(iterations):
        # calculate the matrix-by-vector product Ab
        b_k1 = np.dot(A, b_k)
        # calculate the norm
        b_k1_norm = np.linalg.norm(b_k1)
        # re normalize the vector
        b_k = b_k1 / b_k1_norm
    return b_k
