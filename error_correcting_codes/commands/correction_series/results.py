from argparse import ArgumentError
from collections import namedtuple
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from util.models.result import Result
from util.results.result_series import ResultSeries


class CorrectionSeriesResults(Result):

    result_identifier: str = "correction-series-results"

    def __init__(self, n: int, k: int, j: int, p_values: List[float], num_trials: int):
        self.n = n
        self.k = k
        self.j = j
        self.p_values = p_values
        self.num_trials = num_trials

        self._parity: ResultSeries = ResultSeries("p", p_values, num_trials)
        self._hamming: ResultSeries = ResultSeries("h", p_values, num_trials)

        self.total_results = len(p_values) * num_trials
        self.collected_results = 0

    
    def add_result(self, parity: int, hamming_dist: int, p: float, trial: int):
        self._parity.add_result(parity, p, trial)
        self._hamming.add_result(hamming_dist, p, trial)
        self.collected_results += 1
    
    def get_parity_series(self) -> np.array:
        return self._parity.get_average_series()

    def get_hamming_series(self) -> np.array:
        return self._hamming.get_average_series()
