#!env/bin/python3
import random

import click

from graph_coloring.heuristics.glauber_dyanmics import GlauberDynamics
from graph_coloring.result_models.glauber_dynamics_results import GlauberDynamicsResults
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
@click.option("--delta", required=False, multiple=False, type=int, default=2)
@click.option("--max_iter", required=False, multiple=False, type=int, default=100000)
@click.option("-n", required=False, multiple=False, type=int, default=500)
def glauber_dynamics(verbose, min_n, max_n, step, num_trials, delta, max_iter, n):
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
        raise KeyError("You can't give both one trial and a range of trials!")
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
    results: GlauberDynamicsResults = GlauberDynamicsResults(n_values, num_trials)

    gb: GlauberDynamics = GlauberDynamics()

    for n in n_values:
        for trial in range(num_trials):
            if verbose:
                print(f'[V] Generating graph...')
            generator: PerfectGraphGenerator = PerfectGraphGenerator(n, .5, bool(random.randint(0, 1)))
            G, cheat = generator.generate_random_split_graph()
            gb.run_heuristic(G, {
                'delta': delta,
                'max_iterations': max_iter
            })

            if verbose:
                print(
                    f'[V] Glauber Dynamics found a coloring with {gb.solution.num_conflicting_edges} conflicts on a '
                    f'graph of {len(G)} nodes with chromatic number {cheat} using Max_Deg + {2} colors after '
                    f'{gb.solution.count_recolorings} recolorings.'
                )
            results.add_result(n, trial, gb.solution.count_recolorings)

    store_experiment('graph_coloring', 'Glauber Dynamics Test', results)
