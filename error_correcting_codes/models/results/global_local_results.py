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

    def __init__(self, n: int, k: int, j: int, p_values: List[float]):
        self.n: int = n
        self.k: int= k
        self.j: int= j
        self.p_values: List[float] = p_values

        self.results: Dict[float, List[Tuple[int, int]]] = {}
        self.total_results: int = len(p_values)
        self.collected_results: int = 0

    def add_result(self, values: List[Tuple[int, int]], p: float):
        """
            Adds results, interpreting tuples as (global, local) for each step in the alg.
        """
        if p not in self.p_values:
            raise ArgumentError(f"Bad p value of p={p} provided.")
        if p in self.results.keys():
            raise ArgumentError("Can't set a value which has already been set.")
        self.results[p] = values
        self.collected_results += 1
        

    def get_results(self, p: float):
        if p not in self.p_values:
            raise ArgumentError(f"Bad p value of p={p} provided.")
        return copy(self.results[p])

    def get_global_series(self, p: float):
        if p not in self.p_values:
            raise ArgumentError(f"Bad p value of p={p} provided.")
        return [x[0] for x in self.get_results(p)]

    def get_local_series(self, p: float):
        if p not in self.p_values:
            raise ArgumentError(f"Bad p value of p={p} provided.")
        return [x[1] for x in self.get_results(p)]

    def get_steps(self, p: float):
        if p not in self.p_values:
            raise ArgumentError(f"Bad p value of p={p} provided.")
        return range(len(self.get_results(p)))
