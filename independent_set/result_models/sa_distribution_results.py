import itertools
from datetime import date
from typing import Callable, List, Tuple, Union

import numpy as np

from util.graph.graph import Graph
from util.misc import validate
from util.models.result import Result
from util.results.result_tensor import ResultTensor
from util.tensor import tensor


class SADistributionResults(Result):

    result_identifier: str = "sa-distribution"

    def __init__(self, G: Graph, planted_ind_set: set[int], epsilon: int, num_trials: int, headstart_size: int):
        # Store metadata
        self.G: Graph = G
        self.planted_ind_set = planted_ind_set
        self.epsilon: int = epsilon
        self.num_trials: int = num_trials
        self.headstart_size: int = headstart_size
        # Store trackers for all the stuff we need
        self.vertex_permutations: List[List[int]] = [None] * self.num_trials
        self.final_sizes: List[int] = [None] * self.num_trials
        self.final_intersections: List[int] = [None] * self.num_trials
        self.final_solutions: List[set] = [None] * self.num_trials
        # Mapping from node -> # of times it appears in the final solutions
        self.final_solution_appearances: List[int] = [0] * G.size

    def add_result(self, trial_num: int, vertex_permutation: List[int], solution: set):
        self.vertex_permutations[trial_num] = vertex_permutation
        self.final_sizes[trial_num] = len(solution)
        self.final_intersections[trial_num] = len(set(self.planted_ind_set).intersection(solution))
        self.final_solutions[trial_num] = solution
        for vertex in solution:
            self.final_solution_appearances[vertex] += 1

    def get_num_appearances_for_each_planted_vertex(self) -> List[Tuple[int, int]]:
        """
        List of (vertex, num_appearances) to map out how often each vertex
        appears in the final solution.
        """
        return [(v, self.final_solution_appearances[v]) for v in self.planted_ind_set]
    
    def get_final_sizes_minus_intersections(self) -> List[int]:
        """
        List of (size - intersection) e.g. # of non-planted nodes for each trial. Average to get singular
        number or graph on a line to get an idea about concentration
        """
        return [self.final_sizes[t] - self.final_intersections[t] for t in range(self.num_trials)]
