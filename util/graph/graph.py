import itertools
from typing import List, Set, Tuple

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
        self._max_degree_vertex: int = max(self.vertex_list(), key = lambda v : self.degree(v))
        self._min_degree_vertex: int = min(self.vertex_list(), key = lambda v : self.degree(v))
        self._vertex_list: List[int] = self._graph.nodes
        self._vertex_set: Set[int] = set(self._graph.nodes)


    def degree(self, v: int) -> int:
        return self._graph.degree(v)


    def vertex_list(self) -> List[int]:
        return self._vertex_list


    def vetex_set(self) -> Set[int]:
        return self._vertex_set


    def edge_boundary(self, v: int, subset: Set[int]) -> int:
        """Returns the number of edges between v and set"""
        return len(set(self._graph.neighbors(v)).intersection(subset))
    

    def max_degree(self) -> Tuple[int, int]:
        """Returns (v, deg(v)) where v has the maximum degree and deg(v) is it's degree"""
        return (self._max_degree_vertex, self.degree(self.max_degree_vertex))


    def min_degree(self) -> Tuple[int, int]:
        """Returns (v, deg(v)) where v has the minimum degree and deg(v) is it's degree"""
        return (self._min_degree_vertex, self.degree(self.min_degree_vertex))


    def partition_vertices(self, subset: Set[int]) -> Tuple[Set[int], Set[int]]:
        """
        Returns the vertices of this graph, split into the subset and all other vertices.
        The order is (subset, other_vertices).
        """
        return (subset, self.vertex_set().difference(subset))
