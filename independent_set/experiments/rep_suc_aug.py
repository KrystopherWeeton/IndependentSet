#!env/bin/python3
import copy
import cProfile
import math
import pstats
import random
import sys
from typing import Callable, Set

import click

from independent_set.heuristics.repeated_successive_augmentation import \
    RepeatedSuccessiveAugmentation
from independent_set.heuristics.successive_augmentation import \
    PruningSuccessiveAugmentation
from independent_set.result_models.repeated_suc_aug_results import \
    RepeatedSucAugResults
from independent_set.result_models.sa_distribution_results import \
    SADistributionResults
from util.misc import validate
from util.new_graph.models.graph import generate_planted_ind_set_graph
from util.storage import store_results


def planted_ind_set_size(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 1


class CONSTANTS:
    p: int = 0.5
    headstart_size: int = 5
    max_iterations: int = 5
    init_epsilon: int = 3
    next_epsilon: Callable = lambda x: x - 1 if x > 0 else x


def _v_print(condition: bool, message: str):
    if condition:
        print(f"[V]{message}")

@click.command()
@click.option("-n", required=True, multiple=False, type=int)
@click.option("--num-trials", required=True, multiple=False, type=int)
@click.option("--verbose", required=False, is_flag=True, default=False)
@click.option("--transient", required=False, is_flag=True, default=False)
def repeated_suc_aug(n, num_trials, verbose, transient):
    validate(
        num_trials > 0, f"Unable to run experiment without a positive number of trials."
    )
    validate(n > 0, f"Unable to run experiment with non-positive 0")

    results: RepeatedSucAugResults = RepeatedSucAugResults(n, num_trials)
    alg: RepeatedSuccessiveAugmentation = RepeatedSuccessiveAugmentation(
        max_iterations=CONSTANTS.max_iterations,
        init_epsilon=CONSTANTS.init_epsilon,
        next_epsilon=CONSTANTS.next_epsilon,
        verbose=True,
        debug=True,
    )
    _v_print(verbose, f"Graph Size={n}, Planted Size={planted_ind_set_size(n)}")

    for t in range(num_trials):
        (G, I) = generate_planted_ind_set_graph(n, CONSTANTS.p, planted_ind_set_size(n))
        _v_print(verbose, f"Starting trial {t} / {num_trials}")

        # Define post step hook
        def post_step_hook(S: Set[int], step: int):
            pass

        alg.clear()
        alg.run_heuristic(
            G=G,
            metadata={"intersection_oracle": lambda x: len(x.intersection(I))},
            seed=set(random.sample(I, k=CONSTANTS.headstart_size)),
            post_step_hook=post_step_hook,
        )
        _v_print(verbose, f"Size={len(alg.solution)}, Intersection={len(alg.solution.intersection(I))}")

    if not transient:
        store_results("independent_set", results)
    elif verbose:
        print(f"[V] Skipping store step because transient was set to true.")
