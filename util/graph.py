import copy
import gc
import itertools
import math
import random
import time

from mpmath import mp

mp.dps = 10

from typing import Dict, List, Set, Tuple

import networkx as nx
import numpy as np


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
    raise AttributeError("This function is no longer supported")


def bell_table(n: int) -> list:
    if (n > 3015):
        raise ArithmeticError(f'{n} is larger than what bell table currently supports')

    bell: List[int] = []
    bell_file = open('./graph_coloring/preprocessing_directory/bell_numbers_upto3015.txt', 'r')
    for line in bell_file:
        bell.append(int(line.split()[1]))
    # print('Generated bell table thank god.')
    return bell

    bell: list = [[0 for i in range(n + 1)] for j in range(n + 1)]
    bell[0][0] = 1
    for i in range(1, n + 1):

        # Explicitly fill for j = 0
        bell[i][0] = bell[i - 1][i - 1]

        # Fill for remaining values of j
        for j in range(1, i + 1):
            bell[i][j] = bell[i - 1][j - 1] + bell[i][j - 1]
    return bell


def binom_table(n: int) -> List[List[int]]:
    # r = [[special.comb(j, i) for i in range(n + 1)] for j in range(n + 1)]
    # good_r = [[mp.mpmathify(special.binom(j, i)) for i in range(n + 1)] for j in range(n + 1)]
    # lets try using stirlings formula
    good_r = []
    for j in range(n + 1):
        to_add: list = []
        if j == 0:
            to_add = [0] * (n + 1)
            good_r.append(to_add)
            continue
        for i in range(n + 1):
            if i == 0 or i == j:
                to_add.append(1)
                continue
            if i > j:
                to_add.append(0)
                continue
            to_add.append(
                mp.fmul(
                    to_add[-1],
                    mp.fdiv(
                        mp.fadd(
                            mp.fsub(j, i),
                            1
                        ), i
                    )
                )
            )
            # to_add.append(mp.power(mp.fdiv(mp.fmul(j, math.e), i), i))
        good_r.append(to_add)
    # good_r = [[mp.fdiv(mp.power(mp.fmul(j, math.e), i), i) for i in range(n + 1)] for j in range(n + 1)]
    # assert r == float('inf') or r == good_r
    # print('Generated binom table thank god')
    return good_r


class PerfectGraphGenerator:

    def __init__(self, n: int):
        self.n = n

        # TODO:
        start_time = time.time()
        self.bell = bell_table(self.n)
        self.binom = binom_table(self.n)
        # problem_area: tuple = (self.binomial_coefficient(n, 192), self.bell_number(n - 192), mp.power(2, 192 * (n - 192)))

        self.A = []

        # Fill the A matrix (should take n^2 time I think)
        self.A.append(1)
        for i in range(1, n + 1):
            tosum: list = [mp.fmul(self.binomial_coefficient(i - 1, m), self.A[m]) for m in range(len(self.A))]

            self.A.append(mp.fsum(tosum))

        print(f'finished making tables after {time.time() - start_time} seconds')
        assert mp.fsum(self.A) < mp.inf

    def bell_number(self, n: int) -> int:
        if n < 0:
            raise IndexError("Bell number is not defined for negatives")
        elif n > self.n:
            raise IndexError("Bell number is beyond what we have initialized")
        return self.bell[n]

    # TODO: duplicate, remove?
    def bell_table(n: int) -> list:

        bell: list = [[0 for i in range(n + 1)] for j in range(n + 1)]
        bell[0][0] = 1
        for i in range(1, n + 1):

            # Explicitly fill for j = 0
            bell[i][0] = bell[i - 1][i - 1]

            # Fill for remaining values of j
            for j in range(1, i + 1):
                bell[i][j] = bell[i - 1][j - 1] + bell[i][j - 1]
        return bell

    def get_partition_prob(self, n: int, m: int) -> np.array:

        r: np.array = np.array(
            [float(mp.fmul(self.binomial_coefficient(m - 1, k), mp.fdiv(self.A[k], self.A[m]))) for k in range(m)])
        # r: np.array = np.array([self.binomial_coefficient(m - 1, k) * (self.A[k] / self.A[m]) for k in range(m)])
        r /= r.sum()
        return r

    def generate_random_partition(self, U: [int]) -> List[Set[int]]:
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
            mp.fmul(
                self.binomial_coefficient(n, k), mp.fmul(
                    self.bell_number(n - k), mp.power(2, (k * (n - k)))
                )
            ) for k in range(n + 1)]

        L: mp.mpf = mp.fsum(l)
        probabilities: np.array = np.array([float(mp.fdiv(x, L)) for x in l])
        probabilities /= probabilities.sum()
        k: int = np.random.choice(a=range(n + 1), p=probabilities)
        return int(k)

    def generate_random_unipolar_partition(self, n: int) -> List[Set[int]]:
        k: int = self.get_central_clique_size(n)
        return [set(range(0, k))] + self.generate_random_partition(list(range(k, n)))

    def generate_random_split_graph(
            self,
            p: float = .5,
            co_split: bool = False,
            preset_center_set: int = -1,
            present_side_parts: int = -1) -> [nx.Graph, int]:
        """
        :param: preset_colors: int, maybe we want to plant a coloring
        :return: [nx.Graph, int], generates random perfect graph with a cheat
        """

        # Normal case
        if preset_center_set == -1 and present_side_parts == -1:
            partition: List[Set[int]] = self.generate_random_unipolar_partition(self.n)


        elif preset_center_set != -1 and present_side_parts != -1:
            central_set_size = preset_center_set
            partition: List[Set[int]] = random_k_partition(
                set(range(central_set_size, self.n)),
                present_side_parts
            )
            # Add the central clique to the beginning
            partition.insert(0, set(range(central_set_size)))
        elif preset_center_set == -1:
            central_set_size = preset_center_set
            partition: List[Set[int]] = self.generate_random_partition(list(range(central_set_size, self.n)))
            # Add the central clique to the beginning
            partition.insert(0, set(range(central_set_size)))
        else:
            central_set_size: int = self.get_central_clique_size(self.n)
            partition: List[Set[int]] = random_k_partition(
                set(range(central_set_size, self.n)),
                present_side_parts
            )
            # Add the central clique to the beginning
            partition.insert(0, set(range(central_set_size)))

        S = set()
        for par in partition:
            for el in par:
                S.add(el)
        assert len(S) == self.n

        # print(partition)
        G: nx.Graph = nx.Graph()

        # Either the chromatic number is the number of cliques + 1 or + 0, or it is just the number of independent sets
        # cheat = len(partition) if co_split else max([len(par) for par in partition])

        # Make sure all parts are themselves cliques
        for par in partition:
            par = list(par)
            for i in range(len(par)):
                G.add_node(par[i])
                for j in range(i + 1, len(par)):
                    G.add_edge(par[i], par[j])

        assert len(G) == self.n

        # Add the edges from the central clique
        center: list = partition[0]
        for v in center:
            for par in partition[1:]:
                for u in par:
                    if np.random.binomial(1, p):
                        G.add_edge(u, v)

        G_comp = nx.complement(G)
        # Get size of the max clique of the graph. True method this time.
        max_clique: Set[int] = find_max_stable_set_in_unipolar_graph(G, G_comp, partition) if co_split else (
            find_max_clique_in_unipolar_graph(G, G_comp, partition)
        )

        # for i in max_clique:
        #     for j in max_clique:
        #         if i == j: continue
        #         assert (j not in shc[i] if co_split else j in shc[i])

        # assert len(nx.maximal_independent_set(shc, max_clique)) == len(max_clique)

        G = G_comp if co_split else G

        # assert len(nx.maximal_independent_set(nx.complement(shc), max_clique)) == len(max_clique)

        cheat = len(max_clique)

        # Permute graph
        nodes: list = list(G.nodes)
        permutation = np.random.permutation(nodes)
        # Return permutted graph
        return nx.relabel_nodes(G, dict(zip(nodes, permutation)), copy=True), cheat

    def binomial_coefficient(self, n: int, k: int) -> int:
        return self.binom[n][k]


def find_max_stable_set_in_unipolar_graph(G: nx.Graph, G_comp: nx.Graph, partition: List[Set[int]]) -> Set[int]:
    # Go through each vertex...
    for x in partition[0]:
        side_non_neighbors: Set[int] = set(G_comp[x])
        side_covered: Dict[int, int] = {}
        # ...and take a look at their side neighborhoods...
        for y in side_non_neighbors:
            # ...to see if we cover all the partition with independent vertices
            if y in G[x]:
                continue
            for i in range(1, len(partition)):
                if y in partition[i]:
                    side_covered[i] = y
                    break
        # If we added a num_parts entries to the dictionary, then we made an independent set!
        if len(side_covered.keys()) == len(partition) - 1:
            return set(side_covered.values()).union([x])

    return set([next(iter(part)) for part in partition[1:]])


def find_max_clique_in_unipolar_graph(G: nx.Graph, G_comp: nx.Graph, partition: List[Set[int]]) -> Set[int]:
    # We find minimum vertex covers in shc to get max independent set in G_comp, which gives max clique in shc
    best_max_clique: set = set()
    for i in range(1, len(partition)):
        bipartite_sub = nx.subgraph(G_comp, partition[0].union(partition[i]))
        gc.collect()
        matching = nx.algorithms.bipartite.maximum_matching(bipartite_sub, partition[0])

        max_clique: set = set(bipartite_sub.nodes).difference(nx.algorithms.bipartite.to_vertex_cover(
            bipartite_sub,
            matching,
            partition[0]
        ))
        if len(best_max_clique) < len(max_clique):
            best_max_clique = max_clique

    return best_max_clique


def random_k_partition(S: set, num_colors: int) -> List[Set[int]]:
    if num_colors < 1:
        raise AttributeError('Man, it is not possible to make <1 sets of |S| elements')
    if num_colors > len(S):
        raise AttributeError(f"Man, you can't make {num_colors} non-empty parts of {len(S)} elements!")
    n: int = len(S)
    stirling: np.array = np.zeros((n + 1, n + 1))
    stirling[0, 0] = 1

    for i in range(len(stirling) - 1):
        for j in range(1, len(stirling[i])):
            stirling[i + 1, j] = j * stirling[i, j] + stirling[i, j - 1]

    # Initialize data tables
    parts: int = num_colors
    waiting: List[Tuple[int, int]] = []

    partition: List[Set[int]] = []
    while len(S) != 0 and parts != 1:
        v: int = random.choice(list(S))
        S.discard(v)

        # Either we assign v to its own partition
        # Put v in its own partition with P[Event] = binom_prob
        binom_prob: float = stirling[len(S), parts - 1] / stirling[len(S)][parts] if stirling[len(S), parts] != 0 else 1
        if np.random.binomial(1, p=(binom_prob if (
                binom_prob != None and
                binom_prob != float('NaN') and
                0 <= binom_prob <= 1
        ) else (
                1 if binom_prob >= 1 else 0
        ))):
            partition.append({v})
            parts -= 1
        else:
            waiting.append((v, len(partition)))

    if parts == 1:
        parts -= 1
        partition.append(copy.copy(S))
        S = set()

    assert len(S) == 0 and parts == 0

    for v, starting in waiting:
        partition[random.randrange(starting, len(partition))].add(v)

    return partition


def recursive_random_partition(S: set, num_colors: int) -> List[Set[int]]:
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
        binom_prob: float = stirling[len(S), parts - 1] / stirling[len(S)][parts] if stirling[len(S), parts] != 0 else 1

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


def max_degree(G: nx.Graph) -> int:
    return max(G.degree, key=lambda x: x[1])[1]


def generate_random_color_partition(G: nx.Graph, num_colors: int) -> Dict[int, Set[int]]:
    """
    :param G: nx.Graph
    :param num_colors: int
    :return: dict[int, int], color_to_nodes coloring/partitoning
    """
    # Initialize stirling table
    n: int = len(G)

    partition: List[Set[int]] = random_k_partition(set(G.nodes), num_colors)

    # Make sure its in the right format to return
    coloring: Dict[int, Set[int]] = {}
    for i, color_set in enumerate(partition):
        coloring[i] = color_set
    return coloring


def get_big_independent_set(G: nx.Graph, iterations: int = -1) -> set:
    best_clique = []
    for i in range(iterations if iterations != -1 else len(G) // 2):
        v: int = random.choice(G.nodes)
        maximal_clique: list = nx.maximal_independent_set(G, v)
        if len(best_clique) < len(maximal_clique):
            best_clique = maximal_clique
        if len(best_clique) >= len(G) / 2 - math.sqrt(len(G)):
            break
    return set(best_clique)


def plant_random_hole_in_graph(G: nx.Graph, hole_size: int, anti_hole: int = -1):
    if anti_hole == -1:
        anti_hole = random.randint(0, 1)

    # Choose hole_size-set of nodes
    h = list(random.choices(list(G.nodes), k=hole_size))

    # Delete all the edges in between them
    for i in range(len(h)):
        for j in range(i + 1, len(h)):
            if anti_hole == 1:
                G.add_edge(h[i], h[j])
                continue

            if anti_hole == 0 and h[j] in G[h[i]]:
                G.remove_edge(h[i], h[j])

    # Make a cycle
    for i in range(len(h) - 1):
        if anti_hole == 0:
            G.add_edge(h[i], h[i + 1])
        else:
            G.remove_edge(h[i], h[i + 1])
