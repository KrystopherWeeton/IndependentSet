import itertools
from typing import List, Tuple

import networkx as nx


class Graph(object):

    def __init__(self, seed: nx.Graph):
        self._graph: nx.Graph = seed
        self.size: int = len(self._graph.nodes)
        self._pre_process()


    def _pre_process(self):
        """
        Sets internal trackers at time of graph creation to allow simple
        and quick lookup in the future.
        NOTE: Relies on graphs being an immutable object
        """
        # Calculate maximum and minimum degree vertices
        self.max_degree_vertex: int = max(self.vertices(), key = lambda v : self.degree(v))
        self.min_degree_vertex: int = min(self.vertices(), key = lambda v : self.degree(v))


    def degree(self, v: int) -> int:
        return self._graph.degree(v)


    def vertices(self) -> List[int]:
        return self._graph.nodes


    def make_clique(self, set: set[int]):
        edges = list(itertools.combinations(set, 2))
        self._graph.add_edges_from()


    def edge_boundary(self, v: int, subset: set[int]) -> int:
        """Returns the number of edges between v and set"""
        return len(set(self._graph.neighbors(v)).intersection(subset))
    

    def max_degree(self) -> Tuple[int, int]:
        """Returns (v, deg(v)) where v has the maximum degree and deg(v) is it's degree"""
        return (self.max_degree_vertex, self.degree(self.max_degree_vertex))


    def min_degree(self) -> Tuple[int, int]:
        """Returns (v, deg(v)) where v has the minimum degree and deg(v) is it's degree"""
        return (self.min_degree_vertex, self.degree(self.min_degree_vertex))


