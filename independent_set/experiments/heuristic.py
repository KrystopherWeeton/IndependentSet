#!env/bin/python3
import copy
import cProfile
import math
import pstats
import sys
from typing import List, Set, Tuple

import click

from independent_set.heuristics.fixed_gww import FixedGWW
from independent_set.heuristics.independent_set_heuristic import \
    IndependentSetHeuristic
from independent_set.heuristics.phase_heuristic import PhaseHeuristic
from independent_set.heuristics.successive_augmentation import \
    SuccessiveAugmentation
from independent_set.result_models.heuristic_results import HeuristicResults
from util.new_graph.generator import generate_planted_ind_set_graph
from util.storage import store_results

##########################################
#       Configuration
##########################################

"""
    Provides the size of the planted independent set for a graph with n vertices.
"""
def planted_ind_set_size(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 1


# The probability that edges exist
EDGE_PROBABILITY: float = 0.5
# The maximum number of steps an optimizer can run before we stop it
MAX_OPTIMIZER_STEPS: int = 999
# The percent to accomplish between each print statement
PERCENT_INCREMENT: float = 0.05

# The actual heuristic to run
# ! HEURISTIC: IndependentSetHeuristic = FixedGWW(verbose=True, debug=False)
HEURISTIC: IndependentSetHeuristic = PhaseHeuristic(SuccessiveAugmentation(), FixedGWW(verbose=True, debug=False))
BASE_GWW_METADATA = {
    "num_particles": lambda n: 2 * int(math.sqrt(n)),
    "subset_size": lambda n: int(n ** (2 / 3)),
    "threshold_added_change": 0.0,
    "random_walk_steps": lambda n: int(math.log(n, 2)),
    "min_threshold": 0.1,
}


HEURISTIC: IndependentSetHeuristic = PhaseHeuristic(SuccessiveAugmentation(), SuccessiveAugmentation())
HEURISTIC_METADATA = {
    "metadata": [
        {
            "K": None,
            "epsilon": 3,
            "intersection_oracle": None
        },
        {
            "K": None,
            "epsilon": 0,
            "intersection_oracle": None
        }
    ]
}

"""
HEURISTIC_METADATA: dict = {
    "num_particles":            lambda n: 2 * int(math.sqrt(n)),
    "subset_size":              lambda n: int(n ** (2/3)),
    "threshold_added_change":   0.0,
    "random_walk_steps":        lambda n: int(math.log(n, 2)),
    "min_threshold":            0.1,
}

HEURISTIC: IndependentSetHeuristic = GWW()

HEURISTIC_METADATA: dict = {
    "num_particles":            lambda n: 2 * int(math.sqrt(n)),
    "min_subset_size":          30,
    "threshold_added_change":   0.01,
    "random_walk_steps":        lambda n: int(math.log(n, 2)),
    "min_threshold":            0.1,
}
"""

##########################################
#       Commands / Experiments
##########################################


def run_heuristic(n: List[int], num_trials, verbose) -> HeuristicResults:
    #? Initialization
    results: HeuristicResults = HeuristicResults(n, num_trials, planted_ind_set_size, HEURISTIC_METADATA)
    for n_value in n:
        planted_size: int = planted_ind_set_size(n_value)    
        if planted_size >= n_value:
            print(f"Got a planted size of {planted_size} for n={n_value}. Replacing with maximum planted size of n.")
            planted_size = n_value
        if verbose:
            print(f"Running experiment for n={n_value} with planted_size={planted_size}")
        for t in range(num_trials):
            # Generate a random graph
            (G, B) = generate_planted_ind_set_graph(n_value, EDGE_PROBABILITY, planted_size)
            # Run the heuristic
            HEURISTIC.clear()

            HEURISTIC_METADATA["metadata"][0]["intersection_oracle"] = lambda x : len(x.intersection(B))
            HEURISTIC_METADATA["metadata"][1]["intersection_oracle"] = lambda x : len(x.intersection(B))

            HEURISTIC.run_heuristic(G, HEURISTIC_METADATA)

            # Take the results, collect data, store the results
            solution: set = HEURISTIC.solution.subset
            intersection_size: int = len(solution.intersection(B))
            density: float = G.density(solution)
            subset_size: int = len(solution)
            if verbose:
                print(f"Collected results for n={n_value}, t={t}, with results {intersection_size}, {density}, {subset_size}")
            results.add_result(n_value, t, intersection_size, density, subset_size)
    
    return results


def profile_heuristic():
    profiler = cProfile.Profile()
    profiler.enable()
    profiler.run("run_heuristic([1000], 1, False)")
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()


"""
    Experiment which attempts to solve a planted clique problem from start to end.
"""
@click.command()
@click.option("--profile", required=False, is_flag=True)
@click.option("-n", required=False, multiple=True, type=int)
@click.option("--min-n", required=False, multiple=False, type=int)
@click.option("--max-n", required=False, multiple=False, type=int)
@click.option("--step", required=False, multiple=False, type=int)
@click.option("--num-trials", required=False, multiple=False, type=int, default=1)
@click.option("--transient", required=False, default=False, is_flag=True)
@click.option("--verbose", required=False, is_flag=True, default=False)
def heuristic(profile, n: List[int], min_n, max_n, step, num_trials, transient, verbose):
    #? Check if we are profiling and rec. profile.
    if profile:
        profile_heuristic()
        return

    #? Validate command line arguments
    if len(n) == 0:
        if min_n is None or max_n is None or step is None:
            click.secho("No valid n ranges were provided. Exiting.", fg="red")
            sys.exit(1)
        n = range(min_n, max_n, step)
    if len(n) == 0:
        click.secho("At least one value for n must be provided", fg="red")
    if any([x <= 0 for x in n]):
        click.secho("All values of n must be positive.", fg="red")

    #? Run the heuristic, then persist results
    results = run_heuristic(n, num_trials, verbose) 
    if not transient:
        store_results("independent_set", results)
