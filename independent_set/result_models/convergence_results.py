from datetime import date
from typing import Dict, List, Tuple

import numpy as np

from util.models.result import Result
from util.results.result_tensor import ResultTensor


class ConvergenceResults(Result):

    result_identifier: str = "convergence-results"

    def __init__(self, n_values: List[int], k_values: List[int], seed_int_sizes: List[int], trials: int):
        # Store metadata
        self.trials = trials
        self.n_values = n_values
        self.k_values = k_values
        self.seeed_int_sizes = seed_int_sizes
        self.collected_results = 0
        self.num_results = len(n_values) * trials

        # Indexing is self.results[n] = list of all trial results
        # Each inner list is the num. of non-planted vertices at each step
        # so at convergence, it should hit 0.
        self.results: Dict[int, List[List[int]]] = {}


    def add_result(self, n: int, t: int, value: List[int]):
        if n not in self.n_values or t < 0 or t >= self.trials:
            raise Exception(f"Bad input to add_results n={n}, t={t}")
        if n not in self.results.keys():
            self.results[n] = []
        self.results[n].append(value)
        self.collected_results += 1
    
    def get_results(self, n: int) -> List[List[int]]:
        if n not in self.results.keys():
            raise Exception(f"Bad input for get results n={n}")
        return self.results[n]
