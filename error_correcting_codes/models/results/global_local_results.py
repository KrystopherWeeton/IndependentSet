from argparse import ArgumentError
from collections import namedtuple
from copy import copy
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from error_correcting_codes.models.results.correction_heatmap_results import (
    Dimension, GeneralTensorResults)
from util.misc import construct_list_map
from util.models.result import Result
from util.results.result_tensor import ResultTensor


class GlobalLocalResults(Result):

    result_identifier: str = "global-local-results"

    def __init__(self, n: int, k: int, j: int, p: float, num_trials: int):
        self.n: int = n
        self.k: int = k
        self.j: int = j
        self.p: float = p
        self.num_trials: int = num_trials

        self.results: List[List[Tuple[int, int]]] = []
        self.total_results = num_trials
        self.collected_results: int = 0

    def add_result(self, values: List[Tuple[int, int]], trial: int):
        """
            Adds results, interpreting tuples as (global, local) for each step in the alg.
        """
        self.results.append(values)
        self.collected_results += 1
        
    def get_results(self, t: int):
        return copy(self.results[t])

    def get_global_series(self, t: int):
        return [x[0] for x in self.get_results(t)]

    def get_local_series(self, t: int):
        return [x[1] for x in self.get_results(t)]

    def get_steps(self, t: int):
        return range(len(self.get_results(t)))
