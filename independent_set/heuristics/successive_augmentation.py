import copy
import random
import sys
from typing import Callable, List, Set

from independent_set.heuristics.independent_set_heuristic import \
    IndependentSetHeuristic
from util.models.graph_subset_tracker import GraphSubsetTracker
from util.new_graph.util import greedily_recover_ind_subset


class SuccessiveAugmentation(IndependentSetHeuristic):
    """
    Successive augmentation heuristic which runs successive augmentation on a planted ind
    set problem.

        prune_final_solution        Whether or not to greedily construct final solution out of result
        permute_vertices            Whether or not to permute vertices at the start of each run
    """

    def __init__(self, permute_vertices: bool = False, verbose: bool = False, debug: bool = False):
        super().__init__(
            expected_metadata_keys=[
                "intersection_oracle",
                "epsilon"
            ],
            verbose=verbose,
            debug=debug
        )
        self.permute_vertices: bool = permute_vertices
    

    def _run_heuristic(self, intersection_oracle, epsilon):
        #? Set initial solution to empty value
        if self.solution is None:
            self.solution = set()
        self.node_list = self.G.vertex_list()
        if self.permute_vertices:
            random.shuffle(self.node_list)
        step: int = 0
        for v in self.node_list:
            if v in self.solution:
                continue
            s: int = len(self.solution)
            k: int = intersection_oracle(self.solution)
            threshold: int = max((s - k) /2 - epsilon, 0)
            if self.G.edge_boundary(v, self.solution) <= threshold:
                self.solution.add(v)
            self.call_post_step_hook(self.solution, step)
            step += 1


class PruningSuccessiveAugmentation(SuccessiveAugmentation):

    def __init__(self, permute_vertices: bool = False, verbose: bool = False, debug: bool = False):
        super().__init__(
            permute_vertices=permute_vertices,
            verbose=verbose,
            debug=debug
        )

    
    def _run_heuristic(self, intersection_oracle, epsilon):
        super()._run_heuristic(intersection_oracle, epsilon)
        self.solution = greedily_recover_ind_subset(self.G, GraphSubsetTracker(self.G, self.solution))
