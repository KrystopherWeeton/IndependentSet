from dataclasses import dataclass
from typing import List, Set

import click
import numpy as np

from error_correcting_codes.commands.correction_series.results import \
    CorrectionSeriesResults
from error_correcting_codes.commands.search_space_map.results import \
    SearchSpaceMap
from error_correcting_codes.models.algorithms.greedy import Greedy
from error_correcting_codes.models.algorithms.gww import GWW
from error_correcting_codes.models.codes.ldpc import LDPC, GallagerLDPC
from error_correcting_codes.models.constants import GALLAGHER_PARAMS
from error_correcting_codes.models.message_tracker import MessageTracker
from error_correcting_codes.util import flip_message
from util.array import hamming_dist
from util.models.algorithms.algorithm import Algorithm
from util.profile import profile
from util.storage import store_results


def _run_exp(transient: bool, verbose: bool):
    #?Hyper paramters for gallager exp.
    p: float = GALLAGHER_PARAMS.difficult_p
    NUM_TRIALS: int = 1
    N: int = 1200
    K: int = GALLAGHER_PARAMS.k
    J: int = GALLAGHER_PARAMS.j

    #? Hyper params for go with the winners itself
    random_walk_length: int = 20
    num_particles: int = 50
    """
        See Galalger LDPC for notes on params
    """
    #? -------------------------------------
    results: SearchSpaceMap = SearchSpaceMap(N, K, J, p, NUM_TRIALS)
    for t in range(NUM_TRIALS):
        # Create message and flip it
        code: LDPC = GallagerLDPC(N, J, K)
        message: np.array = np.array([0] * code.msg_len)
        msg_tracker: MessageTracker = MessageTracker(code, message)
        flip_message(msg_tracker, p)

        # Design phase hook to collect particle data
        """
        def phase_hook(particles: List[MessageTracker], threshold: int, max_threshold: int):
            if verbose:
                print(f"[V] Adding results for phase {threshold} / {max_threshold}")
            for p in particles:
                results.add_vertex(
                    p.get_message_string(), 
                    p.get_num_parities_satisifed(), 
                    p.get_hamming_dist_to_original_message(), 
                    t
                )
        """
        def step_hook(msg: MessageTracker):
            results.add_vertex(
                msg.get_message_string(),
                msg.get_num_parities_satisifed(),
                msg.get_hamming_dist_to_original_message(),
                t
            )

        # Run algorithm
        gww: GWW = GWW(verbose=True, debug=False, step_hook=step_hook)
        gww.run(msg=msg_tracker, random_walk_length=2, num_particles=num_particles, init_bit_flip_prob=0)
    
    store_results("error_correcting_codes", results)


@click.command()
@click.option("--transient", required=False, default=False, is_flag=True)
@click.option("--verbose", required=False, is_flag=True, default=False)
def search_space_map(transient, verbose):
    _run_exp(transient, verbose)
