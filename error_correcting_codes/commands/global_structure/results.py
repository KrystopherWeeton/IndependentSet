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


class GlobalStructure(Result):

    result_identifier: str = "global-structure"

    def __init__(self, n: int, k: int, j: int, p: float, ):
        self.n = n
        self.k = k
        self.j = j
        self.p = p
        self._data = {}

    def add_phase(self, pop_inv_ham, pop_parities, exp_parities, max_matching_bits):
        self._data[pop_inv_ham] = {
            "pop_parities": pop_parities,
            "exp_parities": exp_parities,
            "max_matching_bits": max_matching_bits
        }
    
    def finalize(self):
        self.pop_inv_ham = sorted(self._data.keys())
        self.pop_parities = [self._data[x]['pop_parities'] for x in self.pop_inv_ham]
        self.exp_parities = [self._data[x]['exp_parities'] for x in self.pop_inv_ham]
        self.max_matching_bits = [self._data[x]['max_matching_bits'] for x in self.pop_inv_ham]

