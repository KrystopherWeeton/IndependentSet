import random
from typing import Set

from util.graph.graph import Graph


def uniformly_sample_overlap_set(g: Graph, subset: int, overlap: int, non_overlap: int) -> Set[int]:
    """
    Uniformly samples `overlap` elements from `subset` and `non_overlap` elements not from `subset`
    in the provided graph. Returns this subset of `g` as a set.
    """
    _, other_vertices = g.partition_vertices(subset)
    intersection: Set[int] = set(random.sample(subset, overlap))
    disjoint: Set[int] = set(random.sample(other_vertices, non_overlap))
    return intersection.union(disjoint)
