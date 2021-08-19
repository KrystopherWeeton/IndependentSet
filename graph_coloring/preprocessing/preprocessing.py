#!env/bin/python3
import gc
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
        print(f"[V] generating graphs for {n_values} and num_trials={num_trials}")

    graphs: Dict[int, List[Tuple[nx.Graph, int]]] = defaultdict(list)
    comp_split: bool = bool(random.randint(0, 1)) if co_split == -1 else co_split
    generator: PerfectGraphGenerator = None
    for n in n_values:
        generator = PerfectGraphGenerator(n, .5, comp_split)
        for trial in range(num_trials):
            if verbose:
                print(f'[V]: Generating an order {n} graph for trial {trial}...')

            graphs[n].append(generator.generate_random_split_graph())

    del generator
    gc.collect()

    store_preprocessing('graph_coloring', store_name, graphs)
