import random
from argparse import ArgumentError


def coin_flip(success_prob: float) -> bool:
    """
        Returns True with probability `success_prob` and `False` otherwise.
    """
    if success_prob > 1:
        raise ArgumentError(f"Success probability of {success_prob} is larger than 1.")
    return random.random() <= success_prob
