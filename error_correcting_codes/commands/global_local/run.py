from argparse import ArgumentError
from ast import Global
from collections import namedtuple
from dataclasses import dataclass
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
from error_correcting_codes.models.results.global_local_results import \
    GlobalLocalResults
from util.array import hamming_dist
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
    n: int = 1000
    k: int = 5
    j: int = 11
    P_RANGE = np.arange(0.00, 0.5, 0.05)
    """
        See Galalger LDPC for notes on params
    """
    #? -------------------------------------

    code: LDPC = GallagerLDPC(n, j, k)
    results: GlobalLocalResults = GlobalLocalResults(n, k, j, list(P_RANGE))

    for p in list(P_RANGE):
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
