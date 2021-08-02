import random

import click

from graph_coloring.heuristics.basic_local_search import BasicLocalSearch
from graph_coloring.result_models.basic_local_search_results import BasicLocalSearchResults
from util.graph import PerfectGraphGenerator
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
@click.option("-n", required=False, multiple=False, type=int, default=500)
def basic_local_search(verbose, min_n, max_n, step, num_trials, n):
    # TODO: reorder the arguments

    """
        Runs a heuristic for graph coloring, and collects results about start and end coloring metadata
    """
    if (
            (n == None and (min_n == None or max_n == None)) or
            (min_n != None and max_n != None and min_n > max_n)
    ):
        raise KeyError("You gave bad arguments man. n: {}, min_n: {}, max_n: {}".format(n, min_n, max_n))

    if (
            n != None and (min_n != None or max_n != None)
    ):
        n = None
        print('You gave a single n and a range, so we\'re prioritizing the range')
        # raise KeyError("You can't give both one trial and a range of trials!")
    if n == None:
        n_values: [int] = range(min_n, max_n, step)
    else:
        n_values: [int] = [n]
    if n == None:
        n_values: [int] = range(min_n, max_n, step)
    else:
        n_values: [int] = [n]
    if verbose:
        print(f"[V] Running basic heuristic experiment with n values of {n_values} and num_trials={num_trials}")
    results: BasicLocalSearchResults = BasicLocalSearchResults(n_values, num_trials)

    bsl: BasicLocalSearch = BasicLocalSearch()

    for n in n_values:
        for trial in range(num_trials):
            if verbose:
                print(f'[V] Generating graph...')
            generator: PerfectGraphGenerator = PerfectGraphGenerator(n, .5, bool(random.randint(0, 1)))
            G, cheat = generator.generate_random_split_graph()
            if verbose:
                print(f'[V] Graph generated with chromatic number {cheat}.')
            # TODO remove
            # delta = cheat - max_degree(G) - 10
            bsl.run_heuristic(G, {
                'k': cheat,
                'loss_function': l_1_norm
            })

            if verbose:
                print(
                    f'[V] Basic Local Search found a coloring with {bsl.solution.num_conflicting_edges} conflicts on a '
                    f'graph of {len(G)} nodes with chromatic number {cheat} using {cheat} colors after '
                    f'{bsl.solution.calls_to_color_node} recolorings.'
                )
            results.add_result(n, trial, bsl.solution.calls_to_color_node, bsl.solution.num_conflicting_edges)

    store_experiment('graph_coloring', 'Basic Local Search Test', results)


def l_1_norm(original: float, proposed: float) -> float:
    return original - proposed
