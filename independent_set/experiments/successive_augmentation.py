#!env/bin/python3
import copy
import cProfile
import math
import pstats
import random
import sys
import time
from typing import List

import click

from independent_set.heuristics.successive_augmentation import \
    SuccessiveAugmentation
from independent_set.result_models.sa_results import SuccAugResults
from util.misc import guess_timing
from util.models.graph_subset_tracker import GraphSubsetTracker
from util.new_graph.models.graph import generate_planted_ind_set_graph
from util.new_graph.models.ind_boundary_ind_set_graph import \
    generate_planted_ind_set_model
from util.storage import store_results


def planted_ind_set_size(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 1

EDGE_PROBABILITY: float = 0.5
EPSILON: int = 1
HEADSTART_SIZE: int = 5


def run_successive_augmentation(n, num_trials, verbose) -> SuccAugResults:
    #? Run the heuristic, then persist results
    results: SuccAugResults = SuccAugResults(
        n, planted_ind_set_size(n), EPSILON, num_trials, HEADSTART_SIZE
    )
    sa: SuccessiveAugmentation = SuccessiveAugmentation(verbose=True)
    timings: List[float] = []
    for t in results:
        start: float = time.time()

        # Construct graph and run experiment
        (G, B) = generate_planted_ind_set_model(n, EDGE_PROBABILITY, planted_ind_set_size(n))
        sa.clear()

        def post_step_hook(subset: set, step: int):
            results.add_result(step, t, size=len(subset), intersection=len(subset.intersection(B)))

        sa.run_heuristic(
            G, 
            {
                "intersection_oracle": lambda x : len(x.intersection(B)),
                "epsilon": EPSILON
            }, 
            seed=set(random.sample(B, k=HEADSTART_SIZE)), 
            post_step_hook=post_step_hook
        )
        #? Gather final results and store
        intersection_size: int = len(sa.solution.intersection(B))
        size: int = len(sa.solution)
        results.add_final_results(size, intersection_size)
        end: float = time.time()
        timings.append(end - start)
        completed, remaining, upper_bound, total = guess_timing(timings, num_trials)
        if verbose:
            print(f"[V] {t+1} / {num_trials}\tElapsed: {completed:.2f}\tRemaining: {remaining:.2f} ({upper_bound:.2f})\tTotal: {total:.2f}\tSize: {size}\tIntersection: {intersection_size}")
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
    
    results: SuccAugResults = run_successive_augmentation(n, num_trials, verbose)

    if not transient: 
        store_results("independent_set", results)
    elif verbose:
        print(f"[V] Skipping store step because transient was set to true.")
