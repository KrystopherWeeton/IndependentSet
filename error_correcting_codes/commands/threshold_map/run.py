from copy import copy, deepcopy
from dataclasses import dataclass
from email.message import Message
from typing import Dict, List, Set, Tuple

import click
import networkx as nx
import numpy as np

from error_correcting_codes.commands.correction_series.results import \
    CorrectionSeriesResults
from error_correcting_codes.commands.search_space_map.results import \
    SearchSpaceMap
from error_correcting_codes.commands.threshold_map.results import ThresholdMap
from error_correcting_codes.models.algorithms.greedy import Greedy
from error_correcting_codes.models.algorithms.gww import GWW
from error_correcting_codes.models.codes.ldpc import LDPC, GallagerLDPC
from error_correcting_codes.models.constants import GALLAGHER_PARAMS
from error_correcting_codes.models.message_tracker import MessageTracker
from error_correcting_codes.util import flip_message
from util.array import hamming_dist
from util.models.algorithms.algorithm import Algorithm
from util.new_graph.models.graph import Graph
from util.profile import profile
from util.storage import store_results


def score(v: Tuple, code: LDPC) -> int:
    msg: MessageTracker = MessageTracker(code, np.array(v))
    return msg.get_num_parities_satisifed()



def _run_exp(transient: bool, verbose: bool):
    #?Hyper paramters for gallager exp.
    p: float = GALLAGHER_PARAMS.difficult_p
    n: int = 12
    k: int = GALLAGHER_PARAMS.k
    j: int = GALLAGHER_PARAMS.j
    
    min_threshold: int = 4
    max_threshold: int = 13
    #? -------------------------------------
    results: ThresholdMap = ThresholdMap(n, k, j, p)
    code: LDPC = GallagerLDPC(n, j, k)
    N: int = 2**n

    # Construct complete search space graph, score each vertex
    g: nx.graph = nx.hypercube_graph(n)
    scores: Dict[Tuple, int] = {v: score(v, code) for v in g.nodes}

    if verbose:
        print(f"[V] Done Scoring")

    # Adjust graph for each threshold
    for threshold in range(min_threshold, max_threshold):
        nodes: List = deepcopy(g.nodes)
        for v in nodes:
            if scores[v] < threshold:
                g.remove_node(v)
        results.add_search_space(threshold, deepcopy(g))

    store_results("error_correcting_codes", results)


@click.command()
@click.option("--transient", required=False, default=False, is_flag=True)
@click.option("--verbose", required=False, is_flag=True, default=False)
def threshold_map(transient, verbose):
    _run_exp(transient, verbose)
