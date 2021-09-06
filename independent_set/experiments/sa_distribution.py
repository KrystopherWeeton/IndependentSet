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
from independent_set.result_models.sa_distribution_results import \
    SADistributionResults
from util.misc import validate
from util.models.graph_subset_tracker import GraphSubsetTracker
from util.new_graph.generator import generate_planted_ind_set_graph
from util.storage import store_results


def planted_ind_set_size(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 1

EDGE_PROBABILITY: float = 0.5
EPSILON: int = 3
HEADSTART_SIZE: int = 5


"""
    Experiment which attempts to solve a planted clique problem from start to end.
"""
@click.command()
@click.option("-n", required=True, multiple=False, type=int)
@click.option("--num-trials", required=True, multiple=False, type=int)
@click.option("--verbose", required=False, is_flag=True, default=False)
@click.option("--transient", required=False, is_flag=True, default=False)
def sa_distribution(n, num_trials, verbose, transient):
    validate(num_trials > 0, f"Unable to run experiment without a positive number of trials.")
    validate(n > 0, f"Unable to run experiment with non-postivie 0")

    #? Generate graph and then create results object
    G, I = generate_planted_ind_set_graph(n, EDGE_PROBABILITY, planted_ind_set_size(n))
    sa: SuccessiveAugmentation = SuccessiveAugmentation(prune_final_solution=True, permute_vertices=True)
    results: SADistributionResults = SADistributionResults(G, I, EPSILON, num_trials, HEADSTART_SIZE)

    for t in range(num_trials):
        if verbose:
            print(f"[V] Running trial {t+1} / {num_trials}")
        sa.clear()

        sa.run_heuristic(G, {
                "intersection_oracle": lambda x : len(x.intersection(I)),
                "epsilon": EPSILON,
            },
            seed=GraphSubsetTracker(G, set(random.sample(I, k=HEADSTART_SIZE)))
        )
        results.add_result(t, sa.node_list, sa.solution.subset)

    if not transient: 
        store_results("independent_set", results)
    elif verbose:
        print(f"[V] Skipping store step because transient was set to true.")
