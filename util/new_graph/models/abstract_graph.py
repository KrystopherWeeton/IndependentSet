import itertools
from typing import Iterator, List, Set, Tuple

import networkx as nx


class AbstractGraph(object):
    """
    An abstract class which defines the interface through which experiments can 'access' a graph object.
    Each graph interface is free to restrict these access values as they see fit; however, they should
    be clearly documented in the class definition, and where possible should validate the rules of
    access are being followed appropriately.
    """

    def degree(self, v: int) -> int:
        raise NotImplementedError()


    def vertex_list(self) -> List[int]:
        raise NotImplementedError()


    def vertex_set(self) -> Set[int]:
        raise NotImplementedError()


    def edge_boundary(self, v: int, subset: Set[int]) -> int:
        """Returns the number of edges between v and set"""
        raise NotImplementedError()
    

    def max_degree(self) -> Tuple[int, int]:
        """Returns (v, deg(v)) where v has the maximum degree and deg(v) is it's degree"""
        raise NotImplementedError()


    def min_degree(self) -> Tuple[int, int]:
        """Returns (v, deg(v)) where v has the minimum degree and deg(v) is it's degree"""
        raise NotImplementedError()


    def partition_vertices(self, subset: Set[int]) -> Tuple[Set[int], Set[int]]:
        """
        Returns the vertices of this graph, split into the subset and all other vertices.
        The order is (subset, other_vertices).
        """
        raise NotImplementedError()


    def edges(self, subset: Set[int]) -> int:
        """Returns the number of edges in `subset`"""
        raise NotImplementedError()
    

    def pos_edges(self, subset: Set[int]) -> int:
        """Returns the total number of possible edges in the subset"""
        raise NotImplementedError()
    

    def density(self, subset: Set[int]) -> float:
        """Returns the density as `edges/pos_edges` of the `subset`"""
        raise NotImplementedError()


    def neighbors(self, v: int) -> Iterator:
        raise NotImplementedError()
    