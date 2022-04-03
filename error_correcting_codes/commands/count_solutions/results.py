import copy
from argparse import ArgumentError
from collections import namedtuple
from dataclasses import dataclass
from typing import Callable, Dict, List, Set, Tuple

import networkx as nx
import numpy as np
from attr import attr

from util.models.result import Result
from util.new_graph.models.graph import Graph
from util.results.result_series import ResultSeries


class SolutionCount(Result):
    """ Tracks the number of solutions in the search space above the parity threshold """

    result_identifier: str = "threshold-map"

    def __init__(self, n_values: List[int], k: int, j: int, p: float, parity_thresholds: List[int]):
        self.n_values: List[int] = n_values
        self.k: int = k
        self.j: int = j
        self.p: float = p
        self.parity_thresholds: List[int] = parity_thresholds
        if len(parity_thresholds) != len(n_values):
            raise ArgumentError()
        if any([ n % k != 0 for n in self.n_values]):
            raise Exception("N Values must all be divisible by k")
        self.num_solutions: Dict[int, int] = {}

    def add_result(self, n: int, num_solutions: int):
        if n not in self.n_values:
            raise ArgumentError()
        self.num_solutions[n] = num_solutions
    
    def get_series(self) -> Tuple[List[int], List[int]]:
        return (self.n_values, [self.num_solutions[n] for n in self.n_values])
