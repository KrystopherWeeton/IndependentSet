from argparse import ArgumentError

import numpy as np


def randomly_permute_columns(M: np.array) -> np.array:
    return M[:, np.random.permutation(M.shape[1])]


def hamming_dist(x: np.array, y: np.array) -> int:
    if len(x.shape) != 1 or len(y.shape) != 1 or x.shape[0] != y.shape[0]:
        raise ArgumentError(f"Hamming dist requires vectors of equal length, x.shape={x.shape}, y.shape={y.shape}")
    return np.count_nonzero(x != y)
