from copy import copy
from typing import Callable, List, Union

import numpy as np

from util.array import randomly_permute_columns
from util.new_graph.models.bipartite_graph import (BipartiteGenerator,
                                                   BipartiteGraph)

"""
    Abstract class for LDPC code which is represented through a bipartite graph and ldpc matrix
"""
class LDPC:

    def __init__(self, msg_len: int, num_parities: int):
        self.msg_len: int = msg_len
        self.num_parities: int = num_parities
        self._G: BipartiteGraph = None
        self._ldpc_matrix: np.array = None


    def _construct_equiv_ldpc_matrix(self) -> np.array:
        if self._G is None:
            raise Exception("Construct equiv ldpc matrix requires non-None bipartite graph")
        rows: List[List[int]] = []
        for c in self._G.R:
            parity_indices = self._G.neighbors(c)
            rows.append([1 if x in parity_indices else 0 for x in range(0, self.msg_len)])
        return np.array(rows)
    
    def _construct_equiv_bipartite_graph(self) -> BipartiteGraph:
        if self._ldpc_matrix is None:
            raise Exception("Bad input to construct equiv bipartite graph")
        G: BipartiteGraph = BipartiteGenerator.empty_graph(l_size = self.msg_len, r_size = self.num_parities)
        for c in range(self.msg_len):
            for r in range(self.num_parities):
                # Skip over 0 entries
                if self._ldpc_matrix[r][c] == 0:
                    continue
                # Hacky indexing here
                G.add_edge(l=c, r=self.msg_len + r)
        return G
    
    def calculate_parities(self, msg: np.array) -> np.array:
        """ 
            Returns an array of length self.num_parities as 
            an indicator for whether parities are satisfied
        """
        # Use Steven shortcut to fix the indicator array, as without it 0's are used to indicate
        # satisfied parities
        return np.array([1] * self.num_parities) - np.mod(np.matmul(self._ldpc_matrix, msg), 2)

    
    def num_parities_satisfied(self, msg: np.array) -> int:
        return sum(self.calculate_parities(msg))

    
    def get_indices_in_constraint(self, c: int) -> List[int]:
        return self._G.neighbors(c + self.msg_len)

    def get_constraints_for_index(self, index: int) -> List[int]:
        if index < 0 or index >= self.msg_len:
            raise Exception("Out of bounds")
        return [ c - self.msg_len for c in self._G.neighbors(index)]

    def get_constraints(self) -> List[int]:
        """ 
            Returns identifiers for constraints, not guaranteed to be specific numbers.
        """
        return [ c - self.msg_len for c in self._G.R]

    def get_indices(self) -> List[int]:
        """
            Returns indices for the message location. Should be 0 ... message_length - 1
        """
        return self._G.L


"""
    LDPC code which generates tanner graph with fixed edges to generate LDPC code
"""
class TannerLDPC(LDPC):

    def __init__(self, msg_len: int, num_parities: int, edge_count: int):
        super().__init__(msg_len, num_parities)
        self.edge_count = edge_count
        self._G: BipartiteGraph = BipartiteGenerator.l_degree_unif_graph(msg_len, num_parities, edge_count)
        self._ldpc_matrix: np.array = self._construct_equiv_ldpc_matrix()


"""
    LDPC code which creates parity check matrix using Gallager's construction
    NOTE: https://web.stanford.edu/class/ee388/papers/ldpc.pdf
    NOTE: For explanation of n, j, k also reference paper above. Rough translations are provided below
    n: msg_len
    k: Number of bits in each parity check
    j: (kind of) number of parity checks. In actuality it's j * num of rows in each sub-matrix which is
        based on k, so it's j * (n / k)

        rate is 1 - j/k
"""
class GallagerLDPC(LDPC):

    def __construct_seed_matrix(self) -> np.array:
        indices_to_skip: int = 0
        rows: List[List[int]] = []
        while indices_to_skip < self._n-1:
            rows.append(([0] * indices_to_skip) + ([1] * self._k) + ([0] * (self._n - indices_to_skip - self._k)))
            indices_to_skip += self._k
        return np.array(rows)


    def __init__(self, n: int, j: int, k: int):
        super().__init__(msg_len=n, num_parities = j * n // k)
        if n % k != 0:
            raise Exception(f"Gallager construction requires that k be a proper divisor of n, n={n}, k={k}.")
        self._n = n
        self._j = j
        self._k = k

        # Construct appropriate matrix
        seed_matrix: np.array = self.__construct_seed_matrix()       
        self._ldpc_matrix: np.array = copy(seed_matrix)
        for i in range(1, self._j):
            self._ldpc_matrix = np.vstack([self._ldpc_matrix, randomly_permute_columns(copy(seed_matrix))])
        
        self._G: BipartiteGraph = self._construct_equiv_bipartite_graph()
