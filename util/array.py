import numpy as np


def randomly_permute_columns(M: np.array) -> np.array:
    return M[:, np.random.permutation(M.shape[1])]
