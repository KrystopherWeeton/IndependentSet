#!/env/bin/python3

import math
import random
import sys
from pickle import NONE
from typing import List, Set, Tuple

import click

from independent_set.heuristics.independent_set_heuristic import \
    IndependentSetHeuristic
from independent_set.heuristics.swap_hc import SwapHillClimbing
from independent_set.result_models.convergence_results import \
    ConvergenceResults
from util.models.graph_subset_tracker import GraphSubsetTracker
from util.new_graph.models.graph import generate_planted_ind_set_graph
from util.storage import store_results


def calc_k(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 1


def calc_seed_int_size(n: int, k: int) -> int:
    return math.ceil(math.pow(k, 0.5))


EDGE_PROBABILITY: float = 0.5
MAX_LOCAL_OPT_STEPS: int = 9999
DEBUG: bool = False

def generate_seed(size: int, intersection: int, universe: Set[int], planted: Set[int]):
    non_planted: List[int] = list(universe.difference(planted))
    planted: List[int] = list(planted)
    non_planted_seed: Set[int] = set(random.sample(non_planted, size - intersection))
    planted_seed: Set[int] = set(random.sample(planted, intersection))
    return non_planted_seed.union(planted_seed)


@click.command()
@click.option("--min-n", required=True, multiple=False, type=int)
@click.option("--max-n", required=True, multiple=False, type=int)
@click.option("--step", required=True, multiple=False, type=int)
@click.option("--num-trials", required=False, multiple=False, type=int, default=1)
@click.option("--transient", required=False, default=False, is_flag=True)
@click.option("--verbose", required=False, is_flag=True, default=False)
def convergence_speed(min_n: int, max_n: int, step: int, num_trials: int, transient: bool, verbose: bool):
    n_values: List[int] = range(min_n, max_n, step)
    k_values: List[int] = [calc_k(n) for n in n_values]
    seed_int_sizes: List[int] = [calc_seed_int_size(n_values[i], k_values[i]) for i in range(len(n_values))]
    results: ConvergenceResults = ConvergenceResults(n_values, k_values, seed_int_sizes, num_trials)
    # Only run verbose when debugging, because very spammy
    opt: IndependentSetHeuristic = SwapHillClimbing(DEBUG, DEBUG)
    for i in range(len(n_values)):
        n, k, seed_int_size = n_values[i], k_values[i], seed_int_sizes[i]
        if k > n or seed_int_size > k:
            raise Exception(f"Bad planted size n={n}, k={k}, seed_int_size={seed_int_size}")
        for t in range(num_trials):
            opt.clear()
            G, B = generate_planted_ind_set_graph(n, EDGE_PROBABILITY, k)
            seed_set: Set[int] = generate_seed(k, seed_int_size, G.vertex_set(), B)
            seed: GraphSubsetTracker = GraphSubsetTracker(G, seed_set)
            intersection: List[int] = []
            def post_step_hook(S: Set[int], step: int):
                intersection.append(len(S.difference(B)))
            post_step_hook(seed.subset, 0)
            opt.run_heuristic(G=G, post_step_hook=post_step_hook, seed=seed)
            results.add_result(n, t, intersection)
            if verbose:
                print(f"[V] {results.collected_results} / {results.num_results} trials completed")

    if not transient:
        store_results("independent_set", results)
    elif verbose:
        print(f"[V] Skipping store step because transient flag was included.")
