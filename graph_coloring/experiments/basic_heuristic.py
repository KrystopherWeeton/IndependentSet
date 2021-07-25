#!env/bin/python3
import random

import click

from graph_coloring.heuristics.frieze_random_greedy import FriezeRandomGreedy
from graph_coloring.result_models.basic_heuristic_results import BasicHeuristicResults
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
@click.option("-n", required=False, multiple=False, type=int)
@click.option("--min-n", required=False, multiple=False, type=int)
@click.option("--max-n", required=False, multiple=False, type=int)
@click.option("--step", required=False, multiple=False, type=int)
@click.option("--num-trials", required=False, multiple=False, type=int, default=1)
def basic_heuristic(verbose, n, min_n, max_n, step, num_trials):
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
        raise KeyError("You can't give both one trial and a range of trials!")
    if n == None:
        n_values: [int] = range(min_n, max_n, step)
    else:
        n_values: [int] = [n]
    if verbose:
        print(f"[V] Running basic heuristic experiment with n values of {n_values} and num_trials={num_trials}")
    results: BasicHeuristicResults = BasicHeuristicResults(n_values, num_trials)

    # 2. Run experiment
    # TODO: Change to use metadata methodology
    # TODO: needs p value (maybe)
    frg: FriezeRandomGreedy = FriezeRandomGreedy()
    # frg: GuessAndOptimize = GuessAndOptimize()
    for n in n_values:
        for trial in range(num_trials):
            # Generate a random graph with n nodes
            if verbose:
                print(f'[V]: Generating graph...')
            generator: PerfectGraphGenerator = PerfectGraphGenerator(n, .5, bool(random.randint(0, 1)))
            G, cheat = generator.generate_random_split_graph()
            if verbose:
                print(f'[V]: Graph generated with {cheat} colors')

            # Try coloring this graph with frg
            frg.run_heuristic(G)

            # Add to results
            if verbose:
                print(
                    f"[V] The heuristic found a complete proper coloring on a graph of {len(G)} nodes with chromatic "
                    f"number {cheat} using {frg.solution.get_found_chromatic_number()} color(s)")

            results.add_result(n, trial, cheat, frg.solution.get_found_chromatic_number())

    store_experiment("graph_coloring", "test", results)
