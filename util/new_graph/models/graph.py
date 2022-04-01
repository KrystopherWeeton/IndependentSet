import itertools
import random
from copy import copy, deepcopy
from typing import Iterator, List, Set, Tuple

import networkx as nx
import numpy as np

from util.new_graph.models.abstract_graph import AbstractGraph


class Graph(AbstractGraph):

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
        self._vertex_list: List[int] = list(self._graph.nodes)
        self._vertex_set: Set[int] = set(self._graph.nodes)
        self._max_degree_vertex: int = max(self.vertex_list(), key = lambda v : self.degree(v))
        self._min_degree_vertex: int = min(self.vertex_list(), key = lambda v : self.degree(v))


    def degree(self, v: int) -> int:
        return self._graph.degree(v)


    def vertex_list(self) -> List[int]:
        return copy(self._vertex_list)


    def vertex_set(self) -> Set[int]:
        return copy(self._vertex_set)


    def edge_boundary(self, v: int, subset: Set[int]) -> int:
        """Returns the number of edges between v and set"""
        return len(set(self._graph.neighbors(v)).intersection(subset))


    def connected_vertices(self, v: int, subset: Set[int]) -> Set[int]:
        return set(self._graph.neighbors(v)).intersection(subset)


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


    def edges(self, subset: Set[int]) -> int:
        """Returns the number of edges in `subset`"""
        return len(nx.edges(self._graph.subgraph(subset)))
    

    def pos_edges(self, subset: Set[int]) -> int:
        """Returns the total number of possible edges in the subset"""
        return (len(subset) * (len(subset) - 1)) // 2 
    

    def density(self, subset: Set[int]) -> float:
        """Returns the density as `edges/pos_edges` of the `subset`"""
        return self.edges(subset) / self.pos_edges(subset)


    def neighbors(self, v: int) -> Iterator:
        return self._graph.neighbors(v)


    def adjacency_matrix(self) -> np.array:
        return nx.adjacency_matrix(self._graph).toarray()


def generate_erdos_renyi_graph(n: int, p: float) -> Graph:
    """Generates an erdos-renyi graph with `n` vertices and edge probability `p`"""
    return Graph(nx.erdos_renyi_graph(n=n, p=p))


def add_planted_set(g: Graph, size: int, clique: bool) -> Tuple[Graph, Set[int]]:
    """
    Returns a copy of the graph with a planted set that is either a clique
    or an independent set, controlled by the `clique` flag.
    """
    planted: list = random.sample(g.vertex_list(), size)
    edges = list(itertools.combinations(planted, 2))
    new_graph: nx.Graph = deepcopy(g._graph)
    if clique:
        new_graph.add_edges_from(edges)
    else:
        new_graph.remove_edges_from(edges)
    return Graph(new_graph), planted


def generate_planted_ind_set_graph(n: int, p: float, planted_size: int) -> Tuple[Graph, Set[int]]:
    return add_planted_set(generate_erdos_renyi_graph(n, p), size=planted_size, clique=False)


def generate_planted_clique_graph(n: int, p: float, planted_size: int) -> Tuple[Graph, Set[int]]:
    return add_planted_set(generate_erdos_renyi_graph(n, p), size=planted_size, clique=True)
