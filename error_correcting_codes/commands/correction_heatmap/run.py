from argparse import ArgumentError
from typing import List, Tuple

import click
import numpy as np

from error_correcting_codes.models.algorithms.algorithm import Algorithm
from error_correcting_codes.models.algorithms.greedy import Greedy
from error_correcting_codes.models.codes.ldpc import (LDPC, GallagerLDPC,
                                                      TannerLDPC)
from error_correcting_codes.models.message_tracker import MessageTracker
from error_correcting_codes.models.results.correction_heatmap_results import (
    GallagerHeatmapResults, TannerHeatmapResults)
from util.random import coin_flip
from util.storage import store_results

ALG: Algorithm = Greedy(verbose=False, debug=False)

def flip_message(msg_tracker: MessageTracker, p: float) -> List[int]:
    for i in range(msg_tracker.msg_len()):
        if coin_flip(p):
            msg_tracker.swap_index(i)

def run_trial(p: float, code: LDPC):
    # Construct code randomly
    message: List[int] = [0] * code.msg_len
    msg_tracker: MessageTracker = MessageTracker(code, message)
    # Flip message
    flip_message(msg_tracker, p)
    # Run greedy algorithm to fix up
    ALG.run(msg=msg_tracker)
    # See how long the greedy algorithm took / how close it got (hamming distance)
    sol: MessageTracker = ALG.get_solution()
    return sol.get_num_parities_satisifed()



@click.command()
@click.option("--transient", required=False, default=False, is_flag=True)
@click.option("--verbose", required=False, is_flag=True, default=False)
def run_correction_heatmap_tanner(transient, verbose):
    #?Hyper paramters for tanner exp.
    # min, max, step
    P_RANGE = np.arange(0.00, 0.25, 0.05)
    D_RANGE = np.arange(3, 9, 3)
    NUM_TRIALS: int = 10
    N: int = 500

    """
        n = message length
        m = number of parities
        d = edge count (with replacement)
    """
    #? -------------------------------------

    p_values = list(P_RANGE)
    d_values = list(D_RANGE)
    results: TannerHeatmapResults = TannerHeatmapResults(N, d_values, p_values, NUM_TRIALS)
    for p in p_values:
        for d in d_values:
            for t in range(NUM_TRIALS):
                code: LDPC = TannerLDPC(msg_len=N, num_parities = N // 2, edge_count = d)
                results.add_result(run_trial(p, code), d, p, t)
                if verbose:
                    print(f"[V] {results.collected_results} / {results.total_results}")
    if not transient:
        store_results("error_correcting_codes", results)



@click.command()
@click.option("--transient", required=False, default=False, is_flag=True)
@click.option("--verbose", required=False, is_flag=True, default=False)
def run_correction_heatmap_gallager(transient, verbose):
    #?Hyper paramters for gallager exp.
    P_RANGE = np.arange(0.00, 0.25, 0.05)
    NUM_TRIALS: int = 5
    N: int = 500
    K: int = 5    # of bits in each parity check
    J_RANGE = np.arange(1, 10, 4)
    """
        See Galalger LDPC for notes on params
    """
    #? -------------------------------------
    p_values = list(P_RANGE)
    j_values = list(J_RANGE)
    results: GallagerHeatmapResults = GallagerHeatmapResults(N, K, j_values, p_values, NUM_TRIALS)
    for p in p_values:
        for j in j_values:
            for t in range(NUM_TRIALS):
                code: LDPC = GallagerLDPC(N, j, K)
                results.add_result(run_trial(p, code), j, p, t)
                if verbose:
                    print(f"[V] {results.collected_results} / {results.total_results}")
    if not transient:
        store_results("error_correcting_codes", results)
