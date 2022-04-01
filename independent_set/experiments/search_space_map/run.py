from dataclasses import dataclass
from typing import List

import click
import numpy as np

from error_correcting_codes.commands.correction_series.results import \
    CorrectionSeriesResults
from error_correcting_codes.models.algorithms.greedy import Greedy
from error_correcting_codes.models.codes.ldpc import LDPC, GallagerLDPC
from error_correcting_codes.models.message_tracker import MessageTracker
from error_correcting_codes.util import flip_message
from util.array import hamming_dist
from util.profile import profile
from util.storage import store_results


def _run_exp(transient: bool, verbose: bool):
    pass
    #?Hyper paramters for gallager exp.
        P_RANGE = np.arange(0.00, 0.25, 0.03)
        NUM_TRIALS: int = 10
        N: int = 2500
        K: int = 4    # of bits in each parity check
        J: int = 3
        """
            See Galalger LDPC for notes on params
        """
        #? -------------------------------------
        p_values = list(P_RANGE)
        results: CorrectionSeriesResults = CorrectionSeriesResults(N, K, J, p_values, NUM_TRIALS)
        for p in p_values:
            for t in range(NUM_TRIALS):
                code: LDPC = GallagerLDPC(N, J, K)
                r: TrialResult = run_trial(p, code)
                results.add_result(r.parities, r.hamming_dist, p, t)
                if verbose:
                    print(f"[V] {results.collected_results} / {results.total_results}")
        if not transient:
            store_results("error_correcting_codes", results)


@click.command()
@click.option("--transient", required=False, default=False, is_flag=True)
@click.option("--verbose", required=False, is_flag=True, default=False)
def run_correction_series(transient, verbose):
    _run_exp(transient, verbose)
