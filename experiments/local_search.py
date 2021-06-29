#!env/bin/python3
import cProfile, pstats
import subprocess

import math
from typing import Tuple, List
import random

import click
import networkx as nx

from util.graph import generate_planted_independent_set_graph
from util.local_optimization.local_optimization import LocalOptimizer
from util.local_optimization.basic_local_optimizer import BasicLocalOptimizer
from util.local_optimization.all_local_optimizer import AllLocalOptimizer
from util.local_optimization.swap_local_optimizer import SwapLocalOptimizer
from util.local_optimization.metropolis import Metropolis
from util.local_optimization.swap_purge import SwapPurgeLocalOptimizer
from util.storage import store
from util.local_search_results import Results


##########################################
#       Configurations for local optimization
##########################################

# The probability that edges exist
EDGE_PROBABILITY: float = 0.5
# Key provided to every node which is part of the planted independent subset
PLANTED_KEY: str = "beta"
# The step size for k and l
STEP_SIZE: int = 10
# The maximum number of steps an optimizer can run before we stop it
MAX_OPTIMIZER_STEPS: int = 999
# Print debug statements to track what is going on
PRINT_DEBUG: bool = False
# The percent to accomplish between each print statement
PERCENT_INCREMENT: float = 0.05
# local_optimizer: LocalOptimizer = Metropolis(temperature=1)
local_optimizer: LocalOptimizer = SwapPurgeLocalOptimizer(min_subset_size=10)

# ACTUAL RESULTS BOUNDS
# This is the size of the planted independent set in terms of n
def planted_ind_set_size(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 1


# This is the number of 'extra' nodes to include in the initial subset
def l_range(n: int) -> [int]:
    l_init, l_final = (math.ceil(math.log(n)) * 4,  10 * math.ceil(math.sqrt(n)))
    return list(range(l_init, l_final, STEP_SIZE))


# This is the maximum size that we want for the initial intersection size
def k_range(n: int) -> [int]:
    k_init, k_final = (0, math.ceil(math.log(n)) * 4)
    return list(range(k_init, k_final, STEP_SIZE))

"""
# TESTING LOCAL OPTIMIZATION
# This is the size of the planted independent set in terms of n
def planted_ind_set_size(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 4

def l_range(n: int) -> [int]:
    l_init, l_final = (30, 35)
    return list(range(l_init, l_final, STEP_SIZE))


# This is the maximum size that we want for the initial intersection size
def k_range(n: int) -> [int]:
    k_init, k_final = (5, 10)
    return list(range(k_init, k_final, STEP_SIZE))

"""

##########################################
#       Experiments
##########################################

def _local_search(n: [int], num_trials, file_name):
    #? Verify command line arguments make sense
    if len(n) == 0:      # Initial argument checking
        click.secho("At least one value for n must be provided", fg="red")
    if any([x <= 0 for x in n]):
        click.secho("All values of n must be positive.", fg="red")

    #? Initialization
    # random.seed(0)      # TODO: Swap out for randomly seeded randomness when testing is complete
    results: Results = Results(num_trials, n, planted_ind_set_size, k_range, l_range)
    percent_done: float = 0
    results.verify_bounds()                         # Run initial tests just to verify bounds work out
    if PRINT_DEBUG:
        print(f"Verification of k and l values has passed. Starting...")


    #? Loop over the different values of n which should be tested
    for n_value in n:
        # Generate metadata about the trial
        planted_size: int = planted_ind_set_size(n_value)
        planted_size = planted_size if planted_size < n_value else n_value
        if (PRINT_DEBUG):
            print(f"Running experiments for n={n_value} with planted_size={planted_size}")
        
        k_values, l_values = results.get_ranges(n_value)

        for t in range(num_trials):
            # Generate a graph of size n with a planted independent set of a specified size
            (G, B) = generate_planted_independent_set_graph(n_value, EDGE_PROBABILITY, planted_size, "key")

            # Pre-process some data out of G
            erdos_nodes: [int] = set(G.nodes).difference(B)

            for l in l_values:
                for k in k_values:
                    if PRINT_DEBUG:
                        print(f"Running l={l}, k={k}")
                    if len(B) < k:
                        raise RuntimeError("The planted size is smaller than the requested subset size.")
                    if len(erdos_nodes) < l - k:
                        raise RuntimeError(f"Cannot pull {l - k} vertices from {len(erdos_nodes)} vertices.")
                    if l < k:
                        raise RuntimeError(f"Cannot run experiment with l={l} < k={k}")

                    # Generate an initial subset of the graph that has a provided intersection size
                    init_set: set = set(random.sample(erdos_nodes, k=l-k) + random.sample(B, k=k))

                    # Run the local optimizer and collect results
                    final_subset: set = local_optimizer.optimize(initial=init_set, G=G, max_steps = MAX_OPTIMIZER_STEPS)

                    intersection_size: int = len(final_subset.intersection(B))
                    density: float = nx.density(G.subgraph(final_subset))

                    results.add_results(n_value, t, k, l, intersection_size, density, len(final_subset))
                    if results.get_percent_complete() > percent_done + PERCENT_INCREMENT:
                        percent_done = results.get_percent_complete()
                        print(f"{int(percent_done * 100)}% Complete")
    if PRINT_DEBUG:
        print(f"Ranges: {results.ranges}")

    #? Results have been collected. Pickle them into a file for storage so they can be reused
    store(obj=results, file_name=results.generate_file_name(override_name=file_name), directory="results")


@click.command()
@click.option("-n", required=True, multiple=True, type=int)
@click.option("--num-trials", required=False, multiple=False, type=int, default=1)
@click.option("--file-name", required=False, multiple=False, type=str)
@click.option("--profile", required=False, is_flag=True, default=False, help="Run profiler for local search.")
def local_search(n: [int], num_trials, file_name, profile):
    if not profile:
        _local_search(n, num_trials, file_name)
    else:
        profiler = cProfile.Profile()
        profiler.enable()
        _local_search(n=[500], num_trials=1, file_name="profiling")
        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumtime')
        stats.print_stats()