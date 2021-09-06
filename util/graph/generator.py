import itertools
import random
from typing import List, Tuple

import networkx as nx


def generate_erdos_renyi_graph(n: int, p: float) -> Graph:
    """Generates an erdos-renyi graph with `n` vertices and edge probability `p`"""
    return Graph(nx.erdos_renyi_graph(n=n, p=p))


def add_planted_set(g: Graph, size: int, clique: bool) -> Tuple[Graph, set[int]]:
    """
    Returns a copy of the graph with a planted set that is either a clique
    or an independent set, controlled by the `clique` flag.
    """
    planted: list = random.sample(g.vertices(), size)
    edges = list(itertools.combinations(planted, 2))
    if clique:
        return (Graph(g._graph.add_edges_from(edges)), planted)
    else:
        return (Graph(g._graph.remove_edges_from(edges)), planted)


def generate_planted_ind_set_graph(n: int, p: float, planted_size: int) -> Tuple[Graph, set[int]]:
    return add_planted_set(generate_erdos_renyi_graph(n, p), size=planted_size, clique=False)


def generate_planted_clique_graph(n: int, p: float, planted_size: int) -> Tuple[Graph, set[int]]:
    return add_planted_set(generate_erdos_renyi_graph(n, p), size=planted_size, clique=True)
