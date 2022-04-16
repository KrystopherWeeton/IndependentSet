from ast import Global
from copy import deepcopy
from statistics import mean
from typing import Dict, List, Set, Tuple

import click
import networkx as nx
import numpy as np

from error_correcting_codes.commands.global_structure.results import \
    GlobalStructure
from error_correcting_codes.commands.threshold_map.results import ThresholdMap
from error_correcting_codes.models.algorithms.gww import GWW
from error_correcting_codes.models.codes.ldpc import LDPC, GallagerLDPC
from error_correcting_codes.models.constants import GALLAGHER_PARAMS
from error_correcting_codes.models.message_tracker import MessageTracker
from util.array import hamming_dist
from util.models.algorithms.algorithm import Algorithm
from util.profile import profile
from util.random import coin_flip
from util.storage import store_results


def score(v: Tuple, code: LDPC) -> int:
    msg: MessageTracker = MessageTracker(code, np.array(v))
    return msg.get_num_parities_satisifed()

def expected_parities(hamming_distance: int, n: int) -> int:
    return max(int(
        0.75 * (n - hamming_distance) * (n - 2 * hamming_distance) / n
    ), 0)

def flip_message(msg_tracker: MessageTracker, p: float) -> List[int]:
    for i in range(msg_tracker.msg_len()):
        if coin_flip(p):
            msg_tracker.swap_index(i)

@profile
def _run_exp(transient: bool, verbose: bool):
    #? Hyper parameters
    j: int = GALLAGHER_PARAMS.j
    k: int = GALLAGHER_PARAMS.k
    p: float = GALLAGHER_PARAMS.difficult_p
    n: int = 360

    num_particles: int = 100
    random_walk_length: int = 40
    init_bit_flip_prob=0
    #?

    code: LDPC = GallagerLDPC(n=n, j=j, k=k)
    msg: MessageTracker = MessageTracker(code, np.array([0] * n))
    flip_message(msg, p)
    results: GlobalStructure = GlobalStructure(n=n, k=k, j=j, p=p)

    def phase_hook(particles: List[MessageTracker], threshold: int, num_parities: int):
        nonlocal results
        avg_parities: float = mean([p.get_num_parities_satisifed() for p in particles])
        avg_dist: float = mean([p.get_hamming_dist_to_original_message() for p in particles])
        inv_dist: float = n - avg_dist
        if verbose:
            print(f"[V] Adding series data parities={avg_parities}, dist={avg_dist}, min_dist={min([p.get_hamming_dist_to_original_message() for p in particles])}")
        results.add_phase(
            inv_dist, 
            avg_parities, 
            expected_parities(avg_dist, n), 
            max([n - p.get_hamming_dist_to_original_message() for p in particles])
        )

    gww: GWW = GWW(verbose=True, debug=False, step_hook=None, phase_hook=phase_hook)
    if verbose:
        print(f"[V] Running GWW")
    gww.run(msg=msg, random_walk_length=random_walk_length, num_particles=num_particles, init_bit_flip_prob=init_bit_flip_prob)
    results.finalize()
    # Go through saved spots in GWW runs and use local optimization to see what ends up happening if you locally optimize from those spots
    store_results("error_correcting_codes", results)


@click.command()
@click.option("--transient", required=False, default=False, is_flag=True)
@click.option("--verbose", required=False, is_flag=True, default=False)
def global_structure(transient, verbose):
    _run_exp(transient, verbose)
