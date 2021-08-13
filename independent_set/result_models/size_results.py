from datetime import date
from typing import List

import numpy as np

from util.models.result import Result
from util.results.result_tensor import ResultTensor


class SizeResults(Result):

    result_identifier: str = "size-results"

    def __init__(self, n_values: List[int], k_values: List[int], trials: int):
        # Store metadata
        self.trials = trials

        # Store ranges / keys for tracker
        self.n_values = n_values
        self.k_values = k_values
        self.trial_values = list(range(trials))

        # Initialize tracking tensore for the results
        self.result: ResultTensor = ResultTensor()
        self.result.add_dimension("n", self.n_values)
        self.result.add_dimension("k", self.k_values)
        self.result.add_dimension("t", self.trial_values)
        self.result.fix_dimensions()


    def add_result(self, n: int, k: int, t: int, value) -> bool:
        self.result.add_result(value, n=n, k=k, t=t)


    def get_avg_heatmap_values(self):
        if not self.result.all_results_collected():
            raise Warning(f"Attempt to get heatmap values for SizeResults with only {self.result.results_collected} / {self.result.results_total}")
        
        return self.result.collapse_to_matrix()


    def get_results_collected(self) -> int:
        return self.result.results_collected


    def get_total_results(self) -> int:
        return self.result.results_total

    def __iter__(self):
        return iter(self.result.get_index_list())
