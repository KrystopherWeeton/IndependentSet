from typing import List, Tuple

import click
import numpy as np

from error_correcting_codes.models.algorithms.algorithm import Algorithm
from error_correcting_codes.models.algorithms.greedy import Greedy
from error_correcting_codes.models.ldpc import LDPC
from error_correcting_codes.models.message_tracker import MessageTracker
from util.random import coin_flip

# min, max, step
P_RANGE = np.arange(0.00, 1, 0.05)
NUM_TRIALS: int = 10
N: int = 100
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
    print(f"p={p:.2f}\tt={t}: {sol.get_num_parities_satisifed()} / {sol.get_num_parities()}")


@click.command()
def run_correction_heatmap():
    for p in P_RANGE:
        for t in range(NUM_TRIALS):
            run_trial(N, N // 2, D, p, t)
