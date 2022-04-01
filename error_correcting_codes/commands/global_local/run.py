from argparse import ArgumentError
from ast import Global
from collections import namedtuple
from dataclasses import dataclass
from typing import List, Tuple

import click
import numpy as np

from error_correcting_codes.models.algorithms.greedy import Greedy
from error_correcting_codes.models.codes.ldpc import (LDPC, GallagerLDPC,
                                                      TannerLDPC)
from error_correcting_codes.models.constants import GALLAGHER_PARAMS
from error_correcting_codes.models.message_tracker import MessageTracker
from error_correcting_codes.models.results.correction_heatmap_results import (
    GallagerHeatmapResults, TannerHeatmapResults)
from error_correcting_codes.models.results.global_local_results import \
    GlobalLocalResults
from util.array import hamming_dist
from util.models.algorithms.algorithm import Algorithm
from util.random import coin_flip
from util.storage import store_results


def flip_message(msg_tracker: MessageTracker, p: float) -> List[int]:
    for i in range(msg_tracker.msg_len()):
        if coin_flip(p):
            msg_tracker.swap_index(i)

@click.command()
@click.option("--transient", required=False, default=False, is_flag=True)
@click.option("--verbose", required=False, is_flag=True, default=False)
def run_global_local(transient, verbose):
    #?Hyper paramters for gallager exp.
    n: int = 2500
    k: int = GALLAGHER_PARAMS.k
    j: int = GALLAGHER_PARAMS.j
    p: float = GALLAGHER_PARAMS.difficult_p
    num_trials: int = 10
    """
        See Galalger LDPC for notes on params
    """
    #? -------------------------------------

    results: GlobalLocalResults = GlobalLocalResults(n, k, j, p, num_trials)

    for t in range(num_trials):
        code: LDPC = GallagerLDPC(n, j, k)
        series: List[Tuple[int, int]] = []
        message: List[int] = np.array([0] * code.msg_len)
        msg_tracker: MessageTracker = MessageTracker(code, message)

        def step_hook(msg: np.array, parities: int):
            series.append((hamming_dist(message, msg), parities))
        greedy: Algorithm = Greedy(verbose=False, debug=False, step_hook=step_hook)
        flip_message(msg_tracker, p)
        greedy.run(msg=msg_tracker)
        results.add_result(series, p)

        if verbose:
            print(f"[V] {results.collected_results} / {results.total_results}")
        
    if not transient:
        store_results("error_correcting_codes", results)
