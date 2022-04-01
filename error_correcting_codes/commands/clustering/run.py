import itertools
from dataclasses import dataclass
from typing import List, Set

import click
import numpy as np

from error_correcting_codes.commands.clustering.results import ClusteringResult
from error_correcting_codes.commands.correction_series.results import \
    CorrectionSeriesResults
from error_correcting_codes.commands.search_space_map.results import \
    SearchSpaceMap
from error_correcting_codes.models.algorithms.greedy import Greedy
from error_correcting_codes.models.algorithms.gww import GWW
from error_correcting_codes.models.codes.ldpc import LDPC, GallagerLDPC
from error_correcting_codes.models.constants import GALLAGHER_PARAMS
from error_correcting_codes.models.message_tracker import MessageTracker
from error_correcting_codes.util import flip_message, thresholded_random_walk
from util.array import hamming_dist
from util.models.algorithms.algorithm import Algorithm
from util.profile import profile
from util.storage import store_results

"""
    Tests if v1 and v2 are in the same component by doing 'num_walks' walks above 'threshold' and verifying
    that 'perc_walks_threshold' percentage are closer to v2 than v1.
"""
def test_same_cluster(code: LDPC, v1: np.array, v2: np.array, num_walks: int, threshold: int, perc_walks_threshold: float) -> bool:
    successes: int = 0
    for _ in range(num_walks):
        m: MessageTracker = MessageTracker(code, v1)
        thresholded_random_walk(m, threshold, 256)
        v1_dist: int = hamming_dist(v1, m.get_message())
        v2_dist: int = hamming_dist(v2, m.get_message())
        if v2_dist <= v1_dist:
            successes += 1

    print(f"{successes} / {num_walks} : {m.get_message_string()}") 
    if perc_walks_threshold * num_walks <= successes:
        return True
    
    return False



def _run_exp(transient: bool, verbose: bool):
    #?Hyper paramters for gallager exp.
    p: float = GALLAGHER_PARAMS.difficult_p
    NUM_TRIALS: int = 1
    N: int = 12
    K: int = GALLAGHER_PARAMS.k
    J: int = GALLAGHER_PARAMS.j

    # Definitely want to play with this a bit and adjust the threshold
    threshold: int = 6

    #? Hyper params for go with the winners itself
    num_random_walks: int = 100
    """
        See Galalger LDPC for notes on params
    """
    #? -------------------------------------
    results: ClusteringResult = ClusteringResult(N, K, J, p, num_trials=1)

    # Generate code and message, mess with message
    code: LDPC = GallagerLDPC(N, J, K)
    message: np.array = np.array([0] * code.msg_len)
    msg_tracker: MessageTracker = MessageTracker(code, message)
    flip_message(msg_tracker, p)

    # Go through all possible points and validate every point abvoe required threshold
    above_threshold: List[np.array] = []
    for i in range(0, 2**N):
        msg: np.array = np.fromstring(np.binary_repr(i, width=N), dtype=np.uint8) - 48
        # Validate point is above required threshold
        parities_satisfied: int = code.num_parities_satisfied(msg)
        if parities_satisfied >= threshold:
            above_threshold.append(msg)

    # Go through the above threshold points and figure out which ones are actually in the same connected component.    
    for i in above_threshold:
        for j in above_threshold:
            if np.array_equal(i, j):
                continue
            same_cluster: bool = test_same_cluster(code, i, j, 50, threshold, 0.5)
            if same_cluster:
                results.two_vertices_in_cluster(str(i), str(j))

    if not transient:
        store_results("error_correcting_codes", results)


@click.command()
@click.option("--transient", required=False, default=False, is_flag=True)
@click.option("--verbose", required=False, is_flag=True, default=False)
def clustering(transient, verbose):
    _run_exp(transient, verbose)
