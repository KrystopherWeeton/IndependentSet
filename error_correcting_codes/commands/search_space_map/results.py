import copy
from argparse import ArgumentError
from collections import namedtuple
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

import networkx as nx
import numpy as np
from attr import attr

from util.models.result import Result
from util.results.result_series import ResultSeries


class SearchSpace:

    def __init__(self):
        self._search_space: nx.Graph = nx.empty_graph(0)
        self._added_messages: Set[str] = set([])
    
    def add_vertex(self, msg: str, local_score: int, global_score: int) -> bool:
        if msg in self._added_messages:
            #print('repeated msg')
            return False
        self._search_space.add_node(msg, attr={"local": local_score, "global": global_score})
        self._added_messages.add(msg)

        for i in range(len(msg)):
            new: str = "1" if msg[i] == "0" else "0"
            tmp: str = msg[:i] + new + msg[i+1:]
            if tmp in self._added_messages:
                self._search_space.add_edge(msg, tmp)
        return True


class SearchSpaceMap(Result):

    result_identifier: str = "search-space-map"

    def __init__(self, n: int, k: int, j: int, p: float, num_trials: int):
        self.n = n
        self.k = k
        self.j = j
        self.p = p
        self.num_trials = num_trials

        # Create empty graph to represent search space
        self._search_spaces: List[SearchSpace] = [SearchSpace() for t in range(num_trials)]

    def add_vertex(self, msg: str, parities_sat: int, hamming_dist: int, trial: int) -> bool:
        return self._search_spaces[trial].add_vertex(msg, parities_sat, hamming_dist)


    def get_search_space(self, trial: int) -> nx.Graph:
        return self._search_spaces[trial]._search_space
