#!env/bin/python3
import click
import networkx as nx

from graph_coloring.result_models.basic_heuristic_results import BasicHeuristicResults, generate_basic_heuristic_results_file_name
from util.storage import store_experiment

##########################################
#       Configuration
##########################################


##########################################
#       Commands / Experiments
##########################################


@click.command()
@click.option("--verbose", required=False, is_flag=True, default=False)
@click.option("--min-n", required=False, multiple=False, type=int)
@click.option("--max-n", required=False, multiple=False, type=int)
@click.option("--step", required=False, multiple=False, type=int)
@click.option("--num-trials", required=False, multiple=False, type=int, default=1)
def basic_heuristic(verbose, min_n, max_n, step, num_trials):
    """
        Runs a heuristic for graph coloring, and collects results about start and end coloring metadata
    """
    # TODO: Verify arguments passed in min_n < max_n, etc.
    n_values: [int] = range(min_n, max_n, step)
    if verbose:
        print(f"[V] Running basic heuristic experiment with n values of {n_values} and num_trials={num_trials}")
    results: BasicHeuristicResults = BasicHeuristicResults(n_values, num_trials)

    #2. Run experiment

    store_experiment("graph_coloring", "test", results)
