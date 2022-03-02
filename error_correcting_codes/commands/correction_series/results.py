from argparse import ArgumentError
from collections import namedtuple
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from util.misc import construct_list_map
from util.models.result import Result
from util.results.result_tensor import ResultTensor


class SeriesData:

    def __init__(self, x_title: str, x_values: List, num_trials: int):
        self._results: ResultTensor = ResultTensor()
        self._results.add_dimension(x_title, x_values)
        self._results.add_dimension("t", range(num_trials))
        self._results.fix_dimensions()

        self.x_title = x_title
        self.x_values = x_values
        self._x_map = construct_list_map(x_values)
        self.num_trials: int = num_trials

    def add_result(self, y, x, t: int):
        if x not in self.x_values:
            raise ArgumentError()
        if t < 0 or t >= self.num_trials:
            raise ArgumentError()
        self._results.add_result(y, **{self.x_title: self._x_map[x], "t": t})
    
    def get_average_series(self) -> np.array:
        return self._results.collapse_to_list()

class CorrectionSeriesResults(Result):

    result_identifier: str = "correction-series-results"

    def __init__(self, n: int, k: int, j: int, p_values: List[float], num_trials: int):
        self.n = n
        self.k = k
        self.j = j
        self.p_values = p_values
        self.num_trials = num_trials

        self._parity: SeriesData = SeriesData("p", p_values, num_trials)
        self._hamming: SeriesData = SeriesData("h", p_values, num_trials)

        self.total_results = len(p_values)
        self.collected_results = 0

    
    def add_result(self, parity: int, hamming_dist: int, p: float, trial: int):
        self._parity.add_result(parity, p, trial)
        self._parity.add_result(hamming_dist, p, trial)
        self.collected_results += 1
    
    def get_parity_series(self) -> np.array:
        return self._parity.get_average_series()

    def get_hamming_series(self) -> np.array:
        return self._hamming.get_average_series()
