from typing import Callable, List, Union

import numpy as np

from util.new_graph.models.bipartite_graph import (BipartiteGenerator,
                                                   BipartiteGraph)

"""
    Used to generate a DPLC code that can be used to store parities of some bits of messages
    *msg_len*: The length of the message that should be encoded
    *num_parities*: Either the number of pariti
"""
class LDPC:

    def __init__(self, msg_len: int, num_parities: int, edge_count: int):
        self.msg_len = msg_len
        self.num_parities = num_parities
        self.edge_count = edge_count
        self._G: BipartiteGraph = BipartiteGenerator.l_degree_unif_graph(msg_len, num_parities, edge_count)
        self._construct_ldpc_matrix()
    

    def _construct_ldpc_matrix(self):
        rows: List[List[int]] = []
        for c in self._G.R:
            parity_indices = self._G.neighbors(c)
            rows.append([1 if x in parity_indices else 0 for x in range(0, self.msg_len)])
        self._ldpc_matrix = np.array(rows)


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
