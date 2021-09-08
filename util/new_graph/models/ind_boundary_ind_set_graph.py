from typing import List, Set

from numpy import random
from numpy.random import binomial

from util.new_graph.models.graph import Graph


class IndBoundaryIndSetGraph(Graph):
    """
    A graph subclass that allows exclusively for independent queries about edge boundaries,
    with no other information presented. Provides validation for independence of queries.
    Vertices are considered to be [n].

    *PARAMETERS*
    * `n` is the number of vertices in the graph
    * `p` is the edge probability (ind, erdos-renyi)
    * `S` is a subset of vertices with a different edge probability
    * `q` is the edge probability of the special subset
    """

    def __init__(self, n: int, p: float, S: Set[int], q: float):
        # Validate construction arguments
        assert n > 0, f"n must be a positive value. Value provided was {n}"
        assert 0 <= p <= 1, f"p={p} must lie between 0 and 1"
        assert all([1 <= x <= n for x in S]), f"Not all values in S={S} lie in the proper vertex set."
        assert 0 <= q <= 1, f"q={q} must lie between 0 and 1"

        # Store information
        self.n = n
        self.p = p
        self.S = S
        self.s = len(S)
        self.q = q
        self._queried: List[Set(int)] = [set() for x in range(n)]
        self._vertex_list = range(start=1, stop=n+1)
        self._vertex_set = set(self._vertex_list)


    def vertex_list(self) -> List[int]:
        return self._vertex_list


    def vertex_set(self) -> Set[int]:
        return self._vertex_set


    def edge_boundary(self, v: int, subset: Set[int]) -> int:
        """Returns the number of edges between v and set"""
        # Validate trivial bounds
        assert 1 <= v <= self.n, f"Query of {v} is invlaid for a ind-set graph with {self.n} vertices."
        # Validate query is independent of all prior queries
        queried: Set[int] = self._get_queried(v)
        assert queried.isdisjoint(subset), f"Query of non-disjoint subsets"
        self._add_to_queried(subset)
        # Generate a response and return as appropriate.
        in_s: int = len(subset.intersection(self.S))
        out_of_s: int = len(subset) - in_s
        return binomial(out_of_s, self.p) + binomial(in_s, self.q if v in self.S else self.p)


    def _get_queried(self, v: int) -> Set[int]:
        return self._queried[v - 1]


    def _add_to_queried(self, v: int, subset: Set[int]):
        self._queried[v-1].union(subset)



def generate_planted_ind_set_model(n: int, p: float, planted_size: int) -> IndBoundaryIndSetGraph:
    """
    Generates an independent boundary query graph with a planted independent set of
    size `planted_size` and independent edge probability `p` with `n` vertices.
    """
    planted_set: Set[int] = random.sample(range(1, n+1), planted_size)
    return IndBoundaryIndSetGraph(n, p, planted_set, 0)
