import random
from typing import List, Set

from util.models.graph_subset_tracker import GraphSubsetTracker
from util.new_graph.models.graph import Graph


def uniformly_sample_overlap_set(g: Graph, subset: int, overlap: int, non_overlap: int) -> Set[int]:
    """
    Uniformly samples `overlap` elements from `subset` and `non_overlap` elements not from `subset`
    in the provided graph. Returns this subset of `g` as a set.
    """
    _, other_vertices = g.partition_vertices(subset)
    intersection: Set[int] = set(random.sample(subset, overlap))
    disjoint: Set[int] = set(random.sample(other_vertices, non_overlap))
    return intersection.union(disjoint)


def uniformly_sample_subset(g: Graph, size: int) -> Set[int]:
    return set(random.sample(g.vertex_list(), size))



def greedily_recover_ind_subset(g: Graph, subset: GraphSubsetTracker) -> Set[int]:
    """
    Simple greedy algorithm which seeks to recover an independent set through
    sorting the vertices of `subset` in reverse degree order and then going through them
    and greedily selecting vertices to create an independent set.
    """
    sorted_vertices: List[int] = sorted(subset.subset, key=lambda x: subset.internal_degree(x))
    ind_set: Set[int] = set()
    for v in sorted(subset.subset, lambda x: subset.internal_degree(x)):
        if g.edge_boundary(v, ind_set) == 0:
            ind_set.add(v)
    return ind_set
