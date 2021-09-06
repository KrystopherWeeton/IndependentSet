import copy
import random
import sys
from typing import Callable, List

from independent_set.heuristics.independent_set_heuristic import \
    IndependentSetHeuristic
from util.graph.util import greedily_recover_ind_subset
from util.models.graph_subset_tracker import GraphSubsetTracker


class SuccessiveAugmentation(IndependentSetHeuristic):
    """
    Successive augmentation heuristic which runs successive augmentation on a planted ind
    set problem.

        prune_final_solution        Whether or not to greedily construct final solution out of result
        permute_vertices            Whether or not to permute vertices at the start of each run
    """

    def __init__(self, prune_final_solution: bool = False, permute_vertices: bool = False, verbose: bool = False, debug: bool = False):
        super().__init__(
            expected_metadata_keys=[
                "intersection_oracle",
                "epsilon"
            ],
            verbose=verbose,
            debug=debug
        )
        self.prune_final_solution: bool = prune_final_solution
        self.permute_vertices: bool = permute_vertices
    

    def _run_heuristic(self, intersection_oracle, epsilon):
        #? Set initial solution to empty value
        if self.solution is None:
            self.solution: GraphSubsetTracker = GraphSubsetTracker(self.G, set())
        #? Define inclusion predicate
        def f(v, S: GraphSubsetTracker) -> bool:
            threshold: int = max((S.size() - intersection_oracle(S.subset)) / 2 -  epsilon, 0)
            internal_degree: int = S.internal_degree(v)
            return internal_degree <= threshold
        # Generate node list and permute if appropriate 
        self.node_list: List[int] = self.G.vertex_list()
        if self.permute_vertices:
            random.shuffle(self.node_list)
        #? Run successive augmentation
        step: int = 0
        for v in self.node_list:
            if v in self.solution.subset:
                continue
            # Determine whether or not to include v
            include_v = f(v, self.solution)
            if include_v:
                self.solution.add_node(v)
            
            #? Update results
            self.call_post_step_hook(self.solution.subset, step)
            step += 1
        #? Prune final solution if required 
        if self.prune_final_solution:
            self.solution = GraphSubsetTracker(self.G, greedily_recover_ind_subset(self.G, self.solution))
