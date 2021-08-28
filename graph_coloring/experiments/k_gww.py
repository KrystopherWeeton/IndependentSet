import math
import random
from collections import defaultdict
from typing import List, Tuple, Dict

import click
import mpmath
import networkx as nx

from graph_coloring.heuristics.k_gww import K_GWW
from graph_coloring.result_models.basic_local_search_results import BasicLocalSearchResults
from util.graph import PerfectGraphGenerator
from util.storage import load_preprocessing


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
def k_gww(verbose, min_n, max_n, step, num_trials, n, co_split, store_name, pp_file):
    # TODO: reorder the arguments

    """
        Runs a heuristic for graph coloring, and collects results about start and end coloring metadata
    """

    if (pp_file != None and
            (min_n != None or max_n != None or step != None)
    ):
        raise KeyError("You gave a preprocessing arg and some non-preprocessing args. That's illegal man")

    if (
            (pp_file == None and n == None and (min_n == None or max_n == None)) or
            (min_n != None and max_n != None and min_n > max_n)
    ):
        raise KeyError("You gave bad arguments man. n: {}, min_n: {}, max_n: {}".format(n, min_n, max_n))

    if (
            n != None and (min_n != None or max_n != None)
    ):
        n = None
        print('You gave a single n and a range, so we\'re prioritizing the range')
        # raise KeyError("You can't give both one trial and a range of trials!")
    if n == None and pp_file == None:
        n_values: [int] = range(min_n, max_n, step)
    else:
        n_values: [int] = [n]

    graphs: Dict[int, List[Tuple[nx.Graph, int]]] = defaultdict(list)
    co_split: bool = co_split if co_split != -1 else (random.randint(0, 1))
    if pp_file is None:
        for n in n_values:
            generator: PerfectGraphGenerator = PerfectGraphGenerator(n)
            for trial in range(num_trials):
                graphs[n].append(generator.generate_random_split_graph(.5, co_split))
    else:
        graphs = load_preprocessing('graph_coloring', pp_file)
        n_values: List[int] = sorted(graphs.keys())
        num_trials: int = len(list(graphs.items())[0][1])
    if verbose:
        print(f"[V] Running basic heuristic experiment with n values of {n_values} and num_trials={num_trials}")
    results: BasicLocalSearchResults = BasicLocalSearchResults(n_values, num_trials)
    # results: GlauberDynamicsResults = GlauberDynamicsResults(n_values, num_trials)

    gww: K_GWW = K_GWW(verbose=verbose)

    for n in graphs.keys():
        for trial in range(len(graphs[n])):
            if verbose:
                print(f'[V] Generating graph...')
            G, cheat = graphs[n][trial]

            gww.run_heuristic(G, {
                'num_particles': len(G),
                'random_walk_steps': round(mpmath.ln(cheat)),
                'initial_conflict_threshold': round(((n - 1) * math.log(n)) / 2),
                'conflict_threshold_iteration_change': 1,
                'goal_conflict_threshold': 0,
                'k': cheat
            })

            if verbose:
                print(
                    f'[V] Glauber Dynamics found a coloring with {gww.solution.num_conflicting_edges} conflicts on a '
                    f'graph of {len(G)} nodes with chromatic number {cheat} using {cheat} colors after '
                    f'{gww.solution.calls_to_color_node} recolorings.'
                )
