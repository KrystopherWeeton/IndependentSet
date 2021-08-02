#!env/bin/python3
import cProfile
import copy
import math
import pstats
import random
import sys

import click

from util.graph import generate_planted_independent_set_graph
from independent_set.heuristics.successive_augmentation import SuccessiveAugmentation
from independent_set.result_models.suc_aug_concentration_results import (SucAugConcentrationResults,
                                     generate_suc_aug_concentration_results_file_name)
from util.storage import store_experiment
from util.models.graph_subset_tracker import GraphSubsetTracker
from util.misc import validate


def planted_ind_set_size(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 1

EDGE_PROBABILITY: float = 0.5
HEADSTART_SIZE: int = 5

def _run_trial(n: int, planted_size: int, trial_num: int, verbose: bool, result: SucAugConcentrationResults):
    sa: SuccessiveAugmentation = SuccessiveAugmentation()
    if verbose:
        print(f"[V] Running trial {trial_num+1}")

    (G, B) = generate_planted_independent_set_graph(n, EDGE_PROBABILITY, planted_size, "planted")

    # ? For each epsilon value, run the experiment on the SAME Graph provided above
    for epsilon in result.epsilon_values:
        if verbose:
            print(f"[V] Running epsilon={epsilon}")
        sa.clear()

        def post_step_hook(subset: set, step: int):
            result.add_result(epsilon, step, trial_num, size=len(subset), intersection=len(subset.intersection(B)))
        
        sa.run_heuristic(
            G,
            {
                "intersection_oracle": lambda x : len(x.intersection(B)),
                "epsilon": epsilon,
            },
            seed=GraphSubsetTracker(G, set(random.sample(B, k=HEADSTART_SIZE))),
            post_step_hook=post_step_hook
        )


"""
    Experiment which attempts to solve a planted clique problem from start to end.
"""
@click.command()
@click.option("-n",             required=True,  multiple=False, type=int)
@click.option("--min-epsilon",  required=True,  type=int, default=0)
@click.option("--max-epsilon",  required=True,  type=int, default=3)
@click.option("--num-trials",   required=True,  multiple=False, type=int)
@click.option("--verbose",      required=False, is_flag=True, default=False)
@click.option("--transient",    required=False, is_flag=True, default=False)
def suc_aug_concentration(n, min_epsilon, max_epsilon, num_trials, verbose, transient):
    #? Validate arguments
    validate(num_trials > 0, f"Cannot run experiment with ({num_trials} < 1) trials")
    validate(min_epsilon < max_epsilon, f"min_epsilon cannot be less than max_epsilon")
    validate(n > 0, f"n={n} must be positive.")
    planted_size: int = planted_ind_set_size(n)
    result: SucAugConcentrationResults = SucAugConcentrationResults(n, min_epsilon, max_epsilon, num_trials, HEADSTART_SIZE, planted_size)

    for t in result.trial_values:
        _run_trial(n, planted_size, t, verbose, result)
    
    if not transient: 
        store_experiment("independent_set", generate_suc_aug_concentration_results_file_name(), result)
    elif verbose:
        print(f"[V] Skipping store step because transient was set to true.")