from typing import Dict, List

import numpy as np

from util.misc import construct_list_map
from util.models.result import Result
from util.results.result_tensor import ResultTensor


class CorrectionHeatmapResults(Result):

    result_identifier: str = "correction-heatmap-results"

    def __init__(self, n: int, d_values: List[int], p_values: List[float], num_trials: int):
        self.n: int = n
        self.d_values: List[int] = d_values
        self.p_values: List[float] = p_values
        self.t_values: List[int] = list(range(num_trials))
        self._d_map = construct_list_map(d_values)
        self._p_map = construct_list_map(p_values)

        self.total_results = len(d_values) * len(p_values) * num_trials
        self._results = ResultTensor()
        self._results.add_dimension("d", range(len(self.d_values)))
        self._results.add_dimension("p", range(len(self.p_values)))
        self._results.add_dimension("t", range(len(self.t_values)))
        self._results.fix_dimensions()
        self.collected_results: int = 0

    def add_result(self, d: int, p: int, t: int, value: int):
        self._results.add_result(value, d=self._d_map[d], p=self._p_map[p], t=t)
        self.collected_results += 1

    def get_heatmap_data(self) -> List[List[int]]:
        """ Averages over all trials to get the heatmap data """
        return self._results.collapse_to_matrix()
