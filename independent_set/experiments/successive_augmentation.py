#!env/bin/python3
import copy
import cProfile
import math
import pstats
import random
import sys

import click

from independent_set.heuristics.successive_augmentation import \
    SuccessiveAugmentation
from independent_set.result_models.sa_results import SuccAugResults
from util.graph import generate_planted_independent_set_graph
from util.models.graph_subset_tracker import GraphSubsetTracker
from util.storage import store_results


def planted_ind_set_size(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 1

EDGE_PROBABILITY: float = 0.5
EPSILON: int = 1
HEADSTART_SIZE: int = 5


def run_successive_augmentation(n, num_trials, verbose, transient) -> SuccAugResults:
    #? Run the heuristic, then persist results
    results: SuccAugResults = SuccAugResults(
        n, planted_ind_set_size(n), EPSILON, num_trials, HEADSTART_SIZE
    )
    sa: SuccessiveAugmentation = SuccessiveAugmentation(verbose=True)
    for t in results:
        if verbose:
            print(f"[V] Running trial {t + 1} / {num_trials}")

        # Construct graph and run experiment
        (G, B) = generate_planted_independent_set_graph(n, EDGE_PROBABILITY, planted_ind_set_size(n), "planted")
        sa.clear()

        def post_step_hook(subset: set, step: int):
            results.add_result(step, t, size=len(subset), intersection=len(subset.intersection(B)))

        sa.run_heuristic(
            G, 
            {
                "intersection_oracle": lambda x : len(x.intersection(B)),
                "epsilon": EPSILON
            }, 
            seed=GraphSubsetTracker(G, set(random.sample(B, k=HEADSTART_SIZE))), 
            post_step_hook=post_step_hook
        )
        #? Gather final results and store
        intersection_size: int = len(sa.solution.subset.intersection(B))
        size: int = len(sa.solution.subset)
        if verbose:
            print(f"[V] Size={size}, Intersection Size={intersection_size}")
        results.add_final_results(size, intersection_size)
    return results


"""
    Experiment which attempts to solve a planted clique problem from start to end.
"""
@click.command("sa")
@click.option("-n", required=True, multiple=False, type=int)
@click.option("--num-trials", required=True, multiple=False, type=int)
@click.option("--verbose", required=False, is_flag=True, default=False)
@click.option("--transient", required=False, is_flag=True, default=False)
def successive_augmentation(n, num_trials, verbose, transient):
    #? Validate arguments
    if num_trials < 1:
        click.secho("Unable to run experiment without a positive number of trials", fg="red")
        sys.exit(1)
    
    results: SuccAugResults = run_successive_augmentation(n, num_trials, verbose, transient)

    if not transient: 
        store_results("independent_set", results)
    elif verbose:
        print(f"[V] Skipping store step because transient was set to true.")


@click.command()
def profile_successive_augmentation():
    profiler = cProfile.Profile()
    profiler.enable()
    profiler.runctx("run_successive_augmentation(1000, 1, False, True)", globals(), locals())
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()
