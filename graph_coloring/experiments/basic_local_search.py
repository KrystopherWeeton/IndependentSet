import random
from collections import defaultdict
from typing import Dict, List, Tuple

import click
import networkx as nx

from graph_coloring.heuristics.basic_local_search import BasicLocalSearch
from graph_coloring.result_models.basic_local_search_results import \
    BasicLocalSearchResults
from util.graph import PerfectGraphGenerator
from util.storage import store_experiment, load_preprocessing


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
@click.option("--co_split", required=False, multiple=False, type=int, default=-1)
@click.option("--store-name", required=False, multiple=False, type=str, default=None)
@click.option("--pp_file", required=False, multiple=False, type=str, default=None)
def basic_local_search(verbose, min_n, max_n, step, num_trials, n, co_split, store_name, pp_file):
    # TODO: reorder the arguments

    """
        Runs a heuristic for graph coloring, and collects results about start and end coloring metadata
    """

    if (pp_file != None and
            (min_n != None or max_n != None or step != None)
    ):
        raise KeyError("You gave a preprocessing arg and some non-preprocessing args. That's illegal man")

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

    graphs: Dict[int, List[Tuple[nx.Graph, int]]] = defaultdict(list)
    if pp_file is None:
        for n in n_values:
            for trial in range(num_trials):
                co_split: bool = co_split if co_split != -1 else (random.randint(0, 1))
                graphs[n].append(PerfectGraphGenerator(n, .5, co_split).generate_random_split_graph())
    else:
        graphs = load_preprocessing('graph_coloring', pp_file)
        n_values: List[int] = sorted(graphs.keys())
        num_trials: int = len(list(graphs.items())[0][1])

    if verbose:
        print(f"[V] Running basic heuristic experiment with n values of {n_values} and num_trials={num_trials}")
    results: BasicLocalSearchResults = BasicLocalSearchResults(n_values, num_trials)

    bsl: BasicLocalSearch = BasicLocalSearch()

    if pp_file is None:
        for n in n_values:
            for trial in range(num_trials):
                co_split: bool = co_split if co_split != -1 else (random.randint(0, 1))
                graphs[n].append(PerfectGraphGenerator(n, .5, co_split).generate_random_split_graph())
    else:
        graphs = load_preprocessing('graph_coloring', pp_file)

    for n in graphs.keys():
        for trial in range(len(graphs[n])):
            if verbose:
                print(f'[V] Generating graph...')
            G, cheat = graphs[n][trial]
            if verbose:
                print(f'[V] {"co_split" if co_split else "Split"} Graph generated with chromatic number {cheat}.')

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
            results.add_result(n, trial, bsl.solution.calls_to_color_node, bsl.solution.num_conflicting_edges, cheat)

    results_name = store_name if store_name != None else (
        f'min_n{min_n}max_n{max_n}n{n}num_trials{num_trials}co_split{co_split}'
    )

    store_experiment('graph_coloring', results_name, results)


def l_1_norm(original: float, proposed: float) -> float:
    return original - proposed
