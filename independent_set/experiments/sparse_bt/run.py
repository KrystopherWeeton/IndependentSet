from dataclasses import dataclass
from typing import List

import click
import networkx as nx
import numpy as np

from independent_set.algorithms.backtracking import SparseBacktracking
from util.new_graph.models.graph import Graph
from util.profile import profile
from util.storage import store_results

N: int = 50
M: int = 100    # For not just set it to 2N

@profile
def _run_exp(transient: bool, verbose: bool):
    # Construct graph with 4n edges
    # Run backtracking algorith, see how long it takes
    G: Graph = Graph(seed=nx.gnm_random_graph(n=N, m=M))
    ALG: SparseBacktracking = SparseBacktracking(False, False)
    ALG.run(G=G)
    print(f"DONE n={N}, m={M}")
    print(f"Solution: {ALG.get_solution()}")
    print(f"Edges in Solution: {G.edges(ALG.get_solution())}")
    print(f"Calls: {ALG.calls}")


@click.command()
@click.option("--transient", required=False, default=False, is_flag=True)
@click.option("--verbose", required=False, is_flag=True, default=False)
def run_sparse_bt(transient, verbose):
    _run_exp(transient, verbose)
