import itertools
import math
import random

import mpmath

random.seed(1)
from typing import List, Dict
from typing import Set

import networkx as nx
import numpy as np
from scipy import special


# Returns a list of nodes in a random 'headstart' set of size l with k nodes inside the independence set
def get_overlap_set(l: int, k: int, g: nx.graph, planted_key: str) -> list:
    planted: list = nx.get_node_attributes(g, planted_key)
    intersection: list = random.sample(planted, k)
    disjoint = random.sample(set(nx.nodes(g)).difference(intersection))
    return disjoint + intersection


# Generates an erdos_renyi graph with the provided # of vertices
# and edge probabilities.
def generate_erdos_renyi_graph(n: int, p: float) -> nx.Graph:
    return nx.erdos_renyi_graph(n=n, p=p)


# Generates an erdos_renyi graph with the preovided # of vertices
# and edge probabilities (p), with a planted subset of vertices
# that has the preovided edge probabilities (q). The vertices within
# the planted subset have key 'planted_key' attached to them.
def generate_planted_subset_graph(n: int, p: float, q: float, planted_size: int, planted_key: str) -> (nx.Graph, list):
    # ? Perform initial checking to validate input
    if planted_size > n:
        raise RuntimeError(
            f"Attempt to generate a planted subset graph with {planted_size} vertices planted in a graph of size {n}")

    # ? Generate original graph and sample planted set from nodes
    g: nx.Graph = nx.erdos_renyi_graph(n, p)
    planted: list = random.sample(nx.nodes(g), planted_size)

    # ? Remove edges from the planted set
    planted_edges: list = list(itertools.combinations(planted, 2))
    g.remove_edges_from(planted_edges)
    # print(g, dict.fromkeys(planted, planted_key))
    # nx.set_node_attributes(g, dict.fromkeys(planted, {planted_key}))

    # ? Put back the edges with probability q
    for e in planted_edges:
        if random.random() < q:
            g.add_edge(e)

    return g, planted


# Generates a planted independent set graph, similarly to the planted subset
# graph but with 0 edge probabilities within the planted subset
def generate_planted_independent_set_graph(n: int, p: float, planted_size: int, planted_key: str) -> (nx.Graph, list):
    return generate_planted_subset_graph(n, p, 0, planted_size, planted_key)


def count_edge_boundary(G: nx.Graph, v: int, subset: set) -> int:
    return len(set(G.neighbors(v)).intersection(subset))


def binomial_coefficient(n: int, k: int) -> int:
    # since C(n, k) = C(n, n - k)
    # if (k > n - k):
    #     k = n - k
    # # initialize result
    # res = 1
    # # Calculate value of
    # # [n * (n-1) *---* (n-k + 1)] / [k * (k-1) *----* 1]
    # for i in range(k):
    #     res = res * (n - i)
    #     res = res / (i + 1)
    # return res
    raise AttributeError("This function is no longer supported")


# def bell_table(n: int) -> list:
#     bell: list = [[0 for i in range(n + 1)] for j in range(n + 1)]
#     bell[0][0] = 1
#     for i in range(1, n + 1):
#
#         # Explicitly fill for j = 0
#         bell[i][0] = bell[i - 1][i - 1]
#
#         # Fill for remaining values of j
#         for j in range(1, i + 1):
#             bell[i][j] = bell[i - 1][j - 1] + bell[i][j - 1]
#     return bell


def bell_table(n: int) -> List[List[int]]:
    return [[mpmath.bell(i, j) for i in range(n + 1)] for j in range(n + 1)]
    # bell[0][0] = 1
    # for i in range(1, n + 1):
    #
    #     # Explicitly fill for j = 0
    #     bell[i][0] = bell[i - 1][i - 1]
    #
    #     # Fill for remaining values of j
    #     for j in range(1, i + 1):
    #         bell[i][j] = bell[i - 1][j - 1] + bell[i][j - 1]
    # return bell


def binom_table(n: int) -> List[List[int]]:
    return [[special.comb(i, j) for i in range(n + 1)] for j in range(n + 1)]


class PerfectGraphGenerator:

    def __init__(self, n: int, p: float, co_split: bool = 0):
        self.n = n
        self.p = p
        self.co_split = co_split

        # TODO:
        self.bell = bell_table(self.n)
        self.binom = binom_table(self.n)

        self.A = []

        # Fill the A matrix (should take n^2 time I think)
        self.A.append(1)
        for i in range(1, n + 1):
            self.A.append(sum([math.comb(i - 1, m) * self.A[m] for m in range(len(self.A))]))

    def bell_number(self, n: int) -> int:
        if n < 0:
            raise IndexError("Bell number is not defined for negatives")
        elif n > self.n:
            raise IndexError("Bell number is beyond what we have initialized")
        return self.bell[n][0]

    def get_partition_prob(self, n: int, m: int) -> list:

        r = [self.binomial_coefficient(m - 1, k) * (self.A[k] / self.A[m]) for k in range(m)]
        return r

    def generate_random_partition(self, U: [int]) -> list:
        n = len(U)

        # U: list = list(range(n))
        m: int = n
        P: list = []
        while m != 0:
            # Pick a k for this partition
            k: int = np.random.choice(a=range(m), p=self.get_partition_prob(n, m))

            # Sample the partition from what we have left
            l: int = U.pop(np.argmax(U))
            U = list(np.random.permutation(U))
            S = U[:k]

            # Update the partition and our working vars
            P.append(list(list(set(U).difference(set(S))) + [l]))
            U = S
            m = k

        # Pick a random subset for the central clique and put that at the front
        # center: list = P.pop(random.randrange(len(P)))
        # P.insert(0, center)
        return P

    # From https://www2.math.upenn.edu/~wilf/website/Method%20and%20two%20algorithms.pdf
    def get_central_clique_size(self, n: int) -> int:
        l: list = [
            self.binomial_coefficient(n, k) * self.bell_number(n - k) * (2 ** (k * (n - k))) for k
            in range(n + 1)]
        L: int = sum(l)
        k: int = np.random.choice(a=range(n + 1), p=[(x / L) for x in l])
        return int(k)

    def generate_unipolar_partition(self, n: int) -> list:
        k: int = self.get_central_clique_size(n)
        return [list(range(0, k))] + self.generate_random_partition(list(range(k, n)))

    def generate_random_split_graph(self, preset_colors: int = -1) -> [nx.Graph, int]:
        """
        :param: preset_colors: int, maybe we want to plant a coloring
        :return: [nx.Graph, int], generates random perfect graph with a cheat
        """
        if preset_colors == -1:
            partition: list = self.generate_unipolar_partition(self.n)
        else:
            # TODO: Make it so we can plant a color in the base unipolar graph case (not the independent set case)
            self.co_split = True

            # Get central clique size
            central_clique_size: int = self.get_central_clique_size(self.n)

            # Randomly partition the rest of the graph into exactly preset_colors - 1 parts
            partition: List[List[int]] = random_partition(list(range(central_clique_size, self.n)), preset_colors - 1)

            # Add the central clique to the beginning
            partition.insert(0, list(range(central_clique_size)))

        # print(partition)
        G: nx.Graph = nx.Graph()

        # Either the chromatic number is the number of cliques + 1 or + 0, or it is just the number of independent sets
        cheat = len(partition) if self.co_split else max([len(par) for par in partition])

        # Make sure all parts are themselves cliques
        for par in partition:
            par = list(par)
            for i in range(len(par)):
                for j in range(i, len(par)):
                    G.add_edge(par[i], par[j])

        # Add the edges from the central clique
        center: list = partition[0]
        for v in center:
            for par in partition[1:]:
                for u in par:
                    if np.random.binomial(1, self.p):
                        G.add_edge(u, v)

        G = nx.complement(G) if self.co_split else G

        # Permute graph
        nodes: list = list(G.nodes)
        permutation = np.random.permutation(nodes)
        # Return permutted graph
        return nx.relabel_nodes(G, dict(zip(nodes, permutation)), copy=True), cheat

    def binomial_coefficient(self, n: int, k: int) -> int:
        return self.binom[n][k]

def random_partition(S: set, num_colors: int) -> List[Set[int]]:
    """
    :param S: list, set we want to partition
    :param num_colors: int
    :return: dict[int, int], color_to_nodes coloring/partitoning
    """
    # Initialize stirling table
    n: int = len(S)
    stirling: np.array = np.zeros((n + 1, n + 1))
    stirling[0, 0] = 1

    for i in range(len(stirling) - 1):
        for j in range(1, len(stirling[i])):
            stirling[i + 1, j] = j * stirling[i, j] + stirling[i, j - 1]

    def rec_random_partition(S: set, parts: int) -> List[Set[int]]:
        if len(S) == 0 or parts == 0:
            return
        v = random.choice(list(S))
        S.remove(v)

        # Question: Is there a reason why S needs to be a set?
        #   I feel like the reason is a remnant of older code
        #   NOTE: changed to list so I could shuffle it
        if len(S) == 0:
            return [{v}]

        P: List[Set[int]] = []

        # FIXME: For some reason binom probability is greater than 1...
        binom_prob: float = stirling[len(S), parts - 1] / stirling[len(S)][parts] if stirling[len(S), parts] != 0 else 0

        # FIXME: Lets see for now if I can just use sympy stirling
        #   Seems like we can't...

        # binom_prob = stir(len(S), parts - 1) / stir(len(S), parts) if stir(len(S), parts) != 0 else 0

        # Put v in its own partition with P[Event] = binom_prob
        if np.random.binomial(1, p=(binom_prob if (
                binom_prob != None and
                binom_prob != float('NaN') and
                0 <= binom_prob <= 1
        ) else (
                1 if binom_prob >= 1 else 0
        ))):
            new_part: list = list(rec_random_partition(S, parts - 1))
            return [{v}] if new_part == None else [{v}] + new_part

        # Otherwise, we put v into a partition that already exists (meaning we still need to partition into k parts
        P = list(rec_random_partition(S, parts))
        P[random.randrange(len(P))].add(v)

        return P

    return rec_random_partition(S, num_colors)


def generate_random_color_partition(G: nx.Graph, num_colors: int) -> Dict[int, Set[int]]:
    """
    :param G: nx.Graph
    :param num_colors: int
    :return: dict[int, int], color_to_nodes coloring/partitoning
    """
    # Initialize stirling table
    n: int = len(G)

    partition: List[Set[int]] = random_partition(list(G.nodes), num_colors)

    # Make sure its in the right format to return
    coloring: Dict[int, Set[int]] = {}
    for i, color_set in enumerate(partition):
        coloring[i] = color_set
    return coloring
