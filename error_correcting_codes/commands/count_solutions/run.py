import itertools
from copy import deepcopy
from multiprocessing import Pool
from typing import Dict, List, Set, Tuple

import click
import networkx as nx
import numpy as np

from error_correcting_codes.commands.count_solutions.results import \
    SolutionCount
from error_correcting_codes.commands.threshold_map.results import ThresholdMap
from error_correcting_codes.models.algorithms.gww import GWW
from error_correcting_codes.models.codes.ldpc import LDPC, GallagerLDPC
from error_correcting_codes.models.constants import GALLAGHER_PARAMS
from error_correcting_codes.models.message_tracker import MessageTracker
from util.profile import profile
from util.storage import store_results


def score_above_threshold(v: Tuple, code: LDPC, threshold: int) -> bool:
    msg: MessageTracker = MessageTracker(code, np.array(v))
    return msg.get_num_parities_satisifed() >= threshold


#@profile
def _run_exp(transient: bool, verbose: bool):
    #?Hyper paramters for gallager exp.
    p: float = GALLAGHER_PARAMS.difficult_p
    k: int = GALLAGHER_PARAMS.k
    j: int = GALLAGHER_PARAMS.j

    n_values: List[int] = list(range(k, 21, k))
    parity_threshold: List[int] = [n * j // k for n in n_values]
    #? -------------------------------------
    results: SolutionCount = SolutionCount(n_values, k, j, p, parity_threshold)


    for n in n_values:
        code: LDPC = GallagerLDPC(n, j, k)
        threshold: int = parity_threshold

        vectors: List = list(itertools.product([0, 1], repeat=n))
        with Pool(4) as p:
            count = (
                p.starmap(score_above_threshold, [(v, code, threshold) for v in vectors])
            )
            results.add_result(n, count)
        
        if verbose:
            print(f"[V] n={n} complete")
    
    #store_results("error_correcting_codes", results)


@click.command()
@click.option("--transient", required=False, default=False, is_flag=True)
@click.option("--verbose", required=False, is_flag=True, default=False)
def count_solutions(transient, verbose):
    _run_exp(transient, verbose)
