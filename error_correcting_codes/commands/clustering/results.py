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


class ClusteringResult(Result):

    result_identifier: str = "clustering"

    def __init__(self, n: int, k: int, j: int, p: float, num_trials: int):
        self.n = n
        self.k = k
        self.j = j
        self.p = p
        self.num_trials = num_trials

        # Clusters identified with integers beginning from 0, vertices map to cluster index using dictionary
        self.clusters: List[Set[str]] = []
        self.vertex_map: Dict[str, int] = {}


    def add_cluster(self, vertex: str):
        if vertex in self.vertex_map:
            raise Exception()
        self.clusters.append(set([vertex]))
        self.vertex_map[vertex] = len(self.clusters) - 1
    

    def add_to_cluster(self, vertex: str, vertex_in_cluster: str):
        if vertex_in_cluster not in self.vertex_map:
            raise Exception()
        cluster: int = self.vertex_map[vertex_in_cluster]
        self.clusters[cluster].add(vertex)
        self.vertex_map[vertex] = cluster


    def two_vertices_in_cluster(self, v1: str, v2: str):
        # Adds a result, dealing with clustering logic
        if v1 in self.vertex_map and v2 in self.vertex_map:
            if self.vertex_map[v1] != self.vertex_map[v2]:
                print(f"Inconsistent clustering for {v1}, {v2}")
        elif v1 in self.vertex_map and v2 not in self.vertex_map:
            self.add_to_cluster(v2, v1)
        elif v1 not in self.vertex_map and v2 in self.vertex_map:
            self.add_to_cluster(v1, v2)
        else:
            self.add_cluster(v1)
            self.add_to_cluster(v2, v1)
