#!env/bin/python3
import click
import math
import sys
import random
import util.storage as storage
from util.results.sa_results import SuccAugResults, generate_sa_results_file_name
from util.graph import generate_planted_independent_set_graph
from util.heuristics.successive_augmentation import SuccessiveAugmentation
from util.storage import store
import copy

def planted_ind_set_size(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 1

EDGE_PROBABILITY: float = 0.5
BASE_METADATA: dict = {
    "K":                None,
}

"""
    Experiment which attempts to solve a planted clique problem from start to end.
"""
@click.command()
@click.option("-n", required=True, multiple=False, type=int)
@click.option("--num-trials", required=True, multiple=False, type=int)
@click.option("--verbose", required=False, is_flag=True, default=False)
def successive_augmentation(n, num_trials, verbose):
    #? Validate command line arguments
    if num_trials < 1:
        click.secho("Unable to run experiment without a positive number of trials", fg="red")
        sys.exit(1)
    
    #? Run the heuristic, then persist results
    results: SuccAugResults = SuccAugResults(
        n, planted_ind_set_size(n), num_trials
    )
    sa: SuccessiveAugmentation = SuccessiveAugmentation(results)
    for t in results:
        if verbose:
            print(f"[V] Running trial {t + 1} / {num_trials}")

        # Construct graph and run experiment
        (G, B) = generate_planted_independent_set_graph(n, EDGE_PROBABILITY, planted_ind_set_size(n), "planted")
        metadata = copy.copy(BASE_METADATA)
        metadata["K"] = planted_ind_set_size(n)
        metadata["intersection_oracle"] = lambda x : len(x.intersection(B))
        metadata["seed_subset"] = set(random.sample(B, k=5))
        metadata["trial"] = t
        sa.clear()
        sa.run_heuristic(G, metadata)

        if verbose:
            intersection_size: int = len(sa.solution.subset.intersection(B))
            size: int = len(sa.solution.subset)
            print(f"[V] Size={size}, Intersection Size={intersection_size}")
    
    store(obj=results, file_name=generate_sa_results_file_name(), directory="results")