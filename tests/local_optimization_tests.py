import networkx as nx
import random
import numpy as np

import util.local_optimization.local_optimization as loc_opt

def _generate_random_graph(n: int) -> nx.Graph:
    return nx.erdos_renyi_graph(n, 0.5)


def _test_density_after_add() -> int:
    #! TEST: Check that with some random subsets, correct density is determined
    NUM_TRIALS: int = 30
    GRAPH_SIZE: int = 100
    SUBSET_SIZE: int = 30

    G: nx.Graph = _generate_random_graph(GRAPH_SIZE)
    for i in range(NUM_TRIALS):
        subset: [int] = random.sample(G.nodes, SUBSET_SIZE)
        not_in_subset: [int] = [x for x in G.nodes if x not in subset]
        density: float = nx.density(G.subgraph(subset))
        node: int = random.choice(not_in_subset)
        edges_in: int = sum(1 for i in nx.edge_boundary(G, set([node]), subset))
        predicted_density: float = loc_opt.density_after_add(density, 30, edges_in)
        subset.append(node)
        new_density: float = nx.density(G.subgraph(subset))
        assert np.isclose(predicted_density, new_density, atol=1e-08), \
            f"Predicted density of {predicted_density} does not match new" \
            f" density of {new_density}. (edges_in={edges_in}, init_density={density}, subset_size={SUBSET_SIZE})"
    return NUM_TRIALS

def _test_density_after_rem() -> int:
    #! TEST: Check that with some random subsets, correct density is determined
    NUM_TRIALS: int = 30
    GRAPH_SIZE: int = 100
    SUBSET_SIZE: int = 30

    G: nx.Graph = _generate_random_graph(GRAPH_SIZE)
    for i in range(NUM_TRIALS):
        subset: [int] = random.sample(G.nodes, SUBSET_SIZE)
        density: float = nx.density(G.subgraph(subset))
        node: int = random.choice(subset)
        edges_in: int = sum(1 for i in nx.edge_boundary(G, set([node]), subset))
        predicted_density: float = loc_opt.density_after_rem(density, 30, edges_in)
        subset.remove(node)
        new_density: float = nx.density(G.subgraph(subset))
        assert np.isclose(predicted_density, new_density, atol=1e-08), \
            f"Predicted density of {predicted_density} does not match new" \
            f" density of {new_density}. (edges_in={edges_in}, init_density={density}, subset_size={SUBSET_SIZE})"
    return NUM_TRIALS

def _test_density_after_swap() -> int:
    return 0


def run_tests() -> int:
    return _test_density_after_add() + \
            _test_density_after_rem() + \
            _test_density_after_swap()