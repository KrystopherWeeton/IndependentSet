import unittest
from math import sqrt
from typing import List

import numpy as np
from numpy import array

from util.spectral import (adjacency_matrix_eigenvector, is_symmetric,
                           power_iteration)


class TestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.POWER_ITERATION_SAMPLES: int = 100


    def test_is_symmetric(self) -> None:
        I2: array = np.identity(2)
        assert is_symmetric(I2)
        M: array = array([[1, 1], [0, 0]])
        assert not is_symmetric(M)
        T: array = array([[3, 2], [2, 3]])
        assert is_symmetric(T)


    def test_adjacency_matrix_eigenvector(self) -> None:
        A: array = array([[0, 1], [1, 0]])
        t = adjacency_matrix_eigenvector(A, 1)
        assert np.allclose(t, array([1/sqrt(2), 1/sqrt(2)]))

    
    def test_power_iteration(self) -> None:
        A: array = array([[0, 1], [1, 0]])
        # Calcualte principal eigenvector two ways and verify both work
        v1 = adjacency_matrix_eigenvector(A, 1)
        approximations: List[array] = [power_iteration(A, 10) for _ in range(self.POWER_ITERATION_SAMPLES)]
        assert any([np.allclose(v1, v2, atol=0.1) for v2 in approximations])

