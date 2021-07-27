import numpy as np

tensor = np.ndarray

def get_sub_tensor(T: tensor, dimension: int, index: int) -> tensor:
    """
        Returns a sub-tensor restricted to `index` at dimension `dimension`

        Example:

        T = np.ndarray([[1, 2], [3, 4]])        \\
        get_sub_tensor(T, dimension=0, index=0)
        > np.ndarray([1, 3])
    """
    return T.take(indices=index, axis=dimension)
