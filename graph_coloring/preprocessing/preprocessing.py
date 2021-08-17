#!env/bin/python3
import random
from collections import defaultdict
from typing import List, Tuple, Dict

import click
import networkx as nx

from util.graph import PerfectGraphGenerator
from util.storage import store_preprocessing


@click.command()
@click.option("--verbose", required=False, is_flag=True, default=False)
@click.option("-n", required=False, multiple=False, type=int)
@click.option("--min-n", required=False, multiple=False, type=int)
@click.option("--max-n", required=False, multiple=False, type=int)
@click.option("--step", required=False, multiple=False, type=int)
@click.option("--num-trials", required=False, multiple=False, type=int, default=1)
@click.option("--co_split", required=False, multiple=False, type=int, default=-1)
@click.option("--store-name", required=False, multiple=False, type=str, default=None)
def preprocessing(verbose, n, min_n, max_n, step, num_trials, co_split, store_name):
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

    graphs: Dict[int, List[Tuple[nx.Graph, int]]] = defaultdict(list)

    for n in n_values:
        for trial in range(num_trials):
            if verbose:
                print(f'[V]: Generating an order {n} graph for trial {trial}...')

            comp_split: bool = bool(random.randint(0, 1)) if co_split == -1 else co_split
            graphs[n].append(PerfectGraphGenerator(n, .5, comp_split).generate_random_split_graph())

    store_preprocessing('graph_coloring', store_name, graphs)
