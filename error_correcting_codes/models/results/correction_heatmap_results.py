from argparse import ArgumentError
from collections import namedtuple
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from util.misc import construct_list_map
from util.models.result import Result
from util.results.result_tensor import ResultTensor


@dataclass
class Dimension:
    name: str
    values: List[int]

class GeneralTensorResults(Result):

    def __init__(self, *args):
        # Validate arguments
        if any([not isinstance(x, Dimension) for x in args]):
            raise ArgumentError()
        self._dimensions: List[Dimension] = args
        self._dimension_maps: Dict[Dict] = {d.name: construct_list_map(d.values) for d in self._dimensions}
        self.total_results: int = np.prod([len(d.values) for d in self._dimensions])
        self.collected_results: int = 0

        # Initialize results
        self._results = ResultTensor()
        for d in self._dimensions:
            self._results.add_dimension(d.name, range(len(d.values)))
        self._results.fix_dimensions()
    
    def add_result(self, value: int, **kwargs):
        """ NOTE: kwargs should be the keyword args in proper dimensional order """
        self._results.add_result(value, **{name: self._dimension_maps[name][key] for name, key in kwargs.items()})
        self.collected_results += 1

    def get_matrix_data(self) -> List[List[int]]:
        return self._results.collapse_to_matrix()



class HeatmapResults(GeneralTensorResults):

    def __init__(self, dim1: Dimension, dim2: Dimension, num_trials: int):
        super().__init__(dim1, dim2, Dimension("t", range(num_trials)))


class TannerHeatmapResults(Result):

    result_identifier: str = "tanner-heatmap-results"

    def __init__(self, n: int, d_values: List[int], p_values: List[float], num_trials: int):
        self._parity_result: HeatmapResults = HeatmapResults(Dimension("d", d_values), Dimension("p", p_values), num_trials)
        self._hamming_result: HeatmapResults = HeatmapResults(Dimension("d", d_values), Dimension("p", p_values), num_trials)
        self.total_results = self._parity_result.total_results + self._hamming_result.total_results
        self.collected_results = 0
        self.p_values = p_values
        self.d_values = d_values
        self.num_trials = num_trials
        self.n = n
    
    def add_result(self, parity: int, hamming_dist: int, d: int, p: float, t: int):
        self._parity_result.add_result(parity, d=d, p=p, t=t)
        self._hamming_result.add_result(hamming_dist, d=d, p=p, t=t)
        self.collected_results += 1
    
    def get_parity_matrix(self) -> List[List[float]]:
        return self._parity_result.get_matrix_data()

    def get_hamming_matrix(self) -> List[List[float]]:
        return self._hamming_result.get_matrix_data()

class GallagerHeatmapResults(Result):

    result_identifier: str = "gallager-heatmap-results"

    def __init__(self, n: int, k: int, j_values: List[int], p_values: List[float], num_trials: int):
        self._parity_result: HeatmapResults = HeatmapResults(Dimension("j", j_values), Dimension("p", p_values), num_trials)
        self._hamming_result: HeatmapResults = HeatmapResults(Dimension("j", j_values), Dimension("p", p_values), num_trials)
        self.total_results = self._parity_result.total_results + self._hamming_result.total_results
        self.collected_results = 0
        self.n = n
        self.k = k
        self.j_values = j_values
        self.p_values = p_values
        self.num_trials = num_trials
    
    def add_result(self, parity: int, hamming_dist: int, j: int, p: float, t: int):
        self._parity_result.add_result(parity, j=j, p=p, t=t)
        self._hamming_result.add_result(hamming_dist, j=j, p=p, t=t)
        self.collected_results += 1

    def get_parity_matrix(self) -> List[List[float]]:
        return self._parity_result.get_matrix_data()

    def get_hamming_matrix(self) -> List[List[float]]:
        return self._hamming_result.get_matrix_data()
