#!env/bin/python3
import copy
import math

import click

from util.graph import generate_planted_independent_set_graph
from util.heuristics.independent_set_heuristics.fixed_gww import FixedGWW
from util.results.size_results import (SizeResults,
                                       generate_size_results_file_name)
from util.storage import store


def planted_ind_set_size(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 1

EDGE_PROBABILITY: float = 0.5

BASE_METADATA: dict = {
    "num_particles":            lambda n: 2 * int(math.sqrt(n)),
    "subset_size":              None,
    "threshold_added_change":   0.0,
    "random_walk_steps":        lambda n: 3 * int(math.log(n, 2)),
    "min_threshold":            0.1,
    "verbose":                  True, 
}

"""
    Experiment which attempts to solve a planted clique problem from start to end.
"""
@click.command()
@click.option("--verbose",  required=False, is_flag=True,   help="Prints extra output to help track execution.")
@click.option("--min-n",    required=True,  type=int,       help="The min. size of grapht o run GWW with.")
@click.option("--max-n",    required=True,  type=int,       help="The max. size of graph to run GWW with.")
@click.option("--n-step",   required=True,  type=int,       help="The step size to use for n.")
@click.option("--min-k",    required=True,  type=int,       help="The min. size of subset to run GWW with.")
@click.option("--max-k",    required=True,  type=int,       help="The max. size of subset to run GWW with.")
@click.option("--k-step",   required=True,  type=int,       help="The step size for k..")
@click.option("--trials",   required=True,  type=int,       help="The number of trials to run for each k.")
def size(
    verbose,
    min_n,
    max_n,
    n_step,
    min_k,
    max_k,
    k_step,
    trials,
):
    # Print header if doing verbose output
    if verbose:
        print(
                "[V] Running size to see performance of GWW using different fixed set sizes with the following parameters.\n"
                f"[V] {min_n} < n < {max_n} ({n_step})\t\t{min_k} < k < {max_k} ({k_step})\t\ttrials={trials}"
        )

    # Check all parameters passed in
    if min_n > max_n or min_n < 1 or max_n < 1 or n_step < 1 or min_k > max_k or min_k < 1 or max_k < 1 or k_step < 1:
        raise Exception("Bad arguments passed to size experiment.")
    if trials < 1:
        raise Exception("Experiment must be run with a positive number of trials")

    # Create results and run experiment for each possible value
    n_values = range(min_n, max_n + 1, n_step)  # Adjusting for inclusivity
    k_values = range(min_k, max_k + 1, k_step)
    results: SizeResults = SizeResults(n_values=n_values, k_values=k_values, trials=trials)
    gww: FixedGWW = FixedGWW()

    for n, k, t in results:
        # Perform initial calculations and checks
        planted_size = planted_ind_set_size(n)
        if planted_size > n:
            planted_size = n
        if verbose:
            print(f"[V] running trial with n, k, t = {n}, {k}, {t}")

        # Construct metadata, set appropriate subset size
        metadata = copy.copy(BASE_METADATA)
        metadata["subset_size"] = lambda x : k
        
        (G, B) = generate_planted_independent_set_graph(n, EDGE_PROBABILITY, planted_size, "planted")
        gww.clear()
        gww.run_heuristic(G, metadata)

        intersection_size: int = len(gww.solution.subset.intersection(B))
        if verbose:
            print(f"[V] Results: intersection_size of {intersection_size}")
        
        results.add_result(n, k, t, intersection_size)
        if verbose:
            print(f"[V] Collected Results: {results.get_results_collected()} / {results.get_total_results()}")

    store(obj=results, file_name=generate_size_results_file_name(), directory="results")


