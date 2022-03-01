import itertools
import random
from copy import copy, deepcopy
from typing import Iterator, List, Set, Tuple

import networkx as nx
import numpy as np

from util.new_graph.models.graph import Graph


class BipartiteGraph(Graph):

    __VERIFY_STRUCTURE: bool = True

    def __init__(self, seed: nx.Graph, L: Set[int], R: Set[int]):
        # Verify seed is bipartite
        if self.__VERIFY_STRUCTURE:
            if (L.union(R) != set(seed.nodes)):
                raise Exception("Bad bipartite graph created.")
            for u, v in seed.edges:
                if (u in L and v in L) or (u in R and v in R):
                    raise Exception("Bad edge, can't create bipartite graph.")
        self._graph: nx.Graph = seed
        self.l_size: int = len(L)
        self.r_size: int = len(R)
        self.L = L
        self.R = R
        

    def is_left(self, i: int) -> bool:
        return i in self.L
    
    def add_edge(self, l: int, r: int):
        if self.__VERIFY_STRUCTURE:
            if not self.is_left(l) or self.is_left(r):
                raise Exception(f"Bad edge in bipartite graph, l={l}, r={r}, L={self.L}, R={self.R}")
        self._graph.add_edge(l, r)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return nx.is_isomorphic(self._graph, other._graph)
    
    def __ne__(self, other):
        return not self.__eq__(other)

class BipartiteGenerator:
    def __init__(self):
        raise Exception("Abstract class")
    
    @staticmethod
    def empty_graph(l_size: int, r_size: int) -> BipartiteGraph:
        G: nx.graph = nx.empty_graph(n=l_size + r_size)
        nodes: List[int] = list(G.nodes)
        return BipartiteGraph(seed=G, L=set(nodes[0:l_size]), R=set(nodes[l_size:]))
    
    """
        Returns a bipartite graph where each vertex on the left side selects `degree`
        with the vertices that it connects to being chosen uniformly at random `with replacement`.
        Note that this means that multi-edges get collapsed into singular edges.
    """
    @staticmethod
    def l_degree_unif_graph(l_size: int, r_size: int, degree: int) -> BipartiteGraph:
        G: BipartiteGraph = BipartiteGenerator.empty_graph(l_size, r_size)
        for u in G.L:
            # Pick 3 vertices from the other side, with replacement
            L: Set[int] = random.choices(list(G.R), k=degree)
            for v in L:
                G.add_edge(l=u, r=v)
        return G
