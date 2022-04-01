
import random
from typing import List

from error_correcting_codes.models.message_tracker import MessageTracker
from util.random import coin_flip


def flip_message(msg_tracker: MessageTracker, p: float) -> List[int]:
    for i in range(msg_tracker.msg_len()):
        if coin_flip(p):
            msg_tracker.swap_index(i)


"""
    Performs a random walk on the message provided, restricted to not passing below the thresholded # of parities satisfied.
    NOTE: Inclusive of threshold
"""
def thresholded_random_walk(msg: MessageTracker, threshold: int, steps: int):
    # Validate inputs
    if threshold < 0 or steps < 0:
        raise Exception("Bad input")
    if threshold > msg.get_num_parities():
        raise Exception(f"Threshold of {threshold} is too large for {msg.get_num_parities()}")

    msg_len: int = msg.msg_len()

    for _ in range(steps):
        accep_delta: int = msg.get_num_parities_satisifed() - threshold
        parities_swapped: List[int] = msg.get_num_parities_swapped_for_all_indices()
        indices: List[int] = [i for i in range(msg_len) if parities_swapped[i] >= - accep_delta]
        if len(indices) == 0:
            return
        index: int = random.choice(indices)
        msg.swap_index(index)
