from typing import Union, Callable

import networkx as nx

from util.models.graph_subset_tracker import GraphSubsetTracker
from util.heuristics.heuristic import Heuristic


class IndependentSetHeuristic(Heuristic[GraphSubsetTracker]):

    def __init__(self, expected_metadata_keys: [str] = []):
        super().__init__(expected_metadata_keys=expected_metadata_keys)
