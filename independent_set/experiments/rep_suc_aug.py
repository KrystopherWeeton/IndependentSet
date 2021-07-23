#!env/bin/python3
import cProfile
import copy
import math
import pstats
import random
import sys

import click

from util.graph import generate_planted_independent_set_graph
from independent_set.heuristics.repeated_suc_aug import RepeatedSuccessiveAugmentation
from independent_set.result_models.sa_results import (SuccAugResults,
                                     generate_sa_results_file_name)
from util.storage import store_experiment
from util.models.graph_subset_tracker import GraphSubsetTracker


def planted_ind_set_size(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 1

HEADSTART_SIZE: int = 5


def run_successive_augmentation(n, num_trials, verbose, transient) -> SuccAugResults:
    #? Run the heuristic, then persist results
    results: SuccAugResults = SuccAugResults(
        2 * n, planted_ind_set_size(n), num_trials, HEADSTART_SIZE
    )
    sa: RepeatedSuccessiveAugmentation = RepeatedSuccessiveAugmentation()
    #sa: SuccessiveAugmentation = SuccessiveAugmentation()
    for t in results:
        if verbose:
            print(f"[V] Running trial {t + 1} / {num_trials}")

        # Construct graph and run experiment
        (G, B) = generate_planted_independent_set_graph(n, 0.5, planted_ind_set_size(n), "planted")
        metadata = {
            "intersection_oracle": lambda x : len(x.intersection(B)),
            "epsilons": [5, 5],
            "num_repetitions": 2
        }
        sa.clear()

        def post_step_hook(subset: set, step: int):
            results.add_result(step, t, size=len(subset), intersection=len(subset.intersection(B)))

        sa.run_heuristic(G, metadata, seed=GraphSubsetTracker(G, set(random.sample(B, k=HEADSTART_SIZE))), post_step_hook=post_step_hook)
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
@click.command()
@click.option("-n", required=True, multiple=False, type=int)
@click.option("--num-trials", required=True, multiple=False, type=int)
@click.option("--verbose", required=False, is_flag=True, default=False)
@click.option("--transient", required=False, is_flag=True, default=False)
def repeated_suc_aug(n, num_trials, verbose, transient):
    #? Validate arguments
    if num_trials < 1:
        click.secho("Unable to run experiment without a positive number of trials", fg="red")
        sys.exit(1)
    
    results: SuccAugResults = run_successive_augmentation(n, num_trials, verbose, transient)

    if not transient: 
        store_experiment("independent_set", generate_sa_results_file_name(), results)
    elif verbose:
        print(f"[V] Skipping store step because transient was set to true.")