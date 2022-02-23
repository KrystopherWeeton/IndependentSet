from typing import List, Tuple

import click
import numpy as np

from error_correcting_codes.models.algorithms.algorithm import Algorithm
from error_correcting_codes.models.algorithms.greedy import Greedy
from error_correcting_codes.models.ldpc import LDPC
from error_correcting_codes.models.message_tracker import MessageTracker
from error_correcting_codes.models.results.correction_heatmap_results import \
    CorrectionHeatmapResults
from util.random import coin_flip
from util.storage import store_results

# min, max, step
P_RANGE = np.arange(0.00, 1, 0.01)
D_RANGE = np.arange(1, 12, 1)
NUM_TRIALS: int = 25
N: int = 1000
D: int = 6

ALG: Algorithm = Greedy(verbose=False, debug=False)

"""
    n = message length
    m = number of parities
    d = edge count (with replacement)
"""

def flip_message(msg_tracker: MessageTracker, p: float) -> List[int]:
    for i in range(msg_tracker.msg_len()):
        if coin_flip(p):
            msg_tracker.swap_index(i)

def run_trial(n: int, m: int, d: int, p: float, t: int):
    # Construct code randomly
    code: LDPC = LDPC(msg_len=n, num_parities=m, edge_count = d)
    message: List[int] = [0] * n
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
def run_correction_heatmap(transient, verbose):
    p_values = list(P_RANGE)
    d_values = list(D_RANGE)
    results: CorrectionHeatmapResults = CorrectionHeatmapResults(N, d_values, p_values, NUM_TRIALS)

    for p in p_values:
        for d in d_values:
            for t in range(NUM_TRIALS):
                parities_satisfied = run_trial(N, N // 2, d, p, t)
                results.add_result(d, p, t, parities_satisfied)
                if verbose:
                    print(f"[V] {results.collected_results} / {results.total_results}")
    

    if not transient:
        store_results("error_correcting_codes", results)
