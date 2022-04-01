import copy
from argparse import ArgumentError
from collections import namedtuple
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

import networkx as nx
import numpy as np
from attr import attr

from util.models.result import Result
from util.new_graph.models.graph import Graph
from util.results.result_series import ResultSeries


class ThresholdMap(Result):

    result_identifier: str = "threshold-map"

    def __init__(self, n: int, k: int, j: int, p: float):
        self.n = n
        self.k = k
        self.j = j
        self.p = p

        self.search_spaces = {}


    def add_search_space(self, threshold: int, g: nx.graph):
        self.search_spaces[threshold] = g


    def get_search_space(self, threshold: int) -> nx.graph:
        return self.search_spaces[threshold]

    def get_all_thresholds(self) -> List[int]:
        return list(self.search_spaces.keys())
