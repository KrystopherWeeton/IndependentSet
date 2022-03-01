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

    result_identifier: str = None

    def __init__(self, identifier: str, **args):
        # Validate arguments
        if any([not isinstance(Dimension, x) for x in args]):
            raise ArgumentError()
        self.result_identifier = identifier
        self._dimensions: List[Dimension] = args
        self._dimension_maps: Dict[Dict] = {d.name: construct_list_map(d) for d in self._dimensions}
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

    def __init__(self, identifier: str, dim1: Dimension, dim2: Dimension, num_trials: int):
        super().__init__(identifier, dim1, dim2, Dimension("t", range(num_trials)))


class TannerHeatmapResults(HeatmapResults):

    def __init__(self, n: int, d_values: List[int], p_values: List[float], num_trials: int):
        super().__init__("tanner-heatmap-results", Dimension("d", d_values), Dimension("p", p_values), num_trials)
        self.n = n
    
    def add_result(self, value: int, d: int, p: float, t: int):
        super().add_result(value, d=d, p=p, t=t)


class GallagerHeatmapResults(HeatmapResults):
    def __init__(self, n: int, k: int, j_values: List[int], p_values: List[float], num_trials: int):
        super().__init__("gallager-heatmap-results", Dimension("j", j_values), Dimension("p", p_values, num_trials))
        self.n = n
        self.k = k
    
    def add_result(self, value: int, j: int, p: float, t: int):
        super().add_result(value, j=j, p=p, t=t)
