from typing import List

import numpy as np

from util.misc import construct_list_map
from util.results.result_tensor import ResultTensor


class ResultSeries:

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
            raise Exception()
        if t < 0 or t >= self.num_trials:
            raise Exception()
        self._results.add_result(y, **{self.x_title: x, "t": t})
    
    def get_average_series(self) -> np.array:
        return self._results.collapse_to_list()
