import sys
from typing import Callable

from util.graph import count_edge_boundary
from independent_set.heuristics.independent_set_heuristic import IndependentSetHeuristic
from util.models.graph_subset_tracker import GraphSubsetTracker


class SuccessiveAugmentation(IndependentSetHeuristic):
    """
    Successive augmentation heuristic which runs successive augmentation on a planted ind
    set problem. Uses `prune_final_solution` to determine whether or not to greedily
    find a planted_independent subset in the final solution.
    """

    def __init__(self, prune_final_solution: bool = False):
        super().__init__(
            expected_metadata_keys=[
                "intersection_oracle",
                "epsilon"
            ]
        )
        self.prune_final_solution: bool = prune_final_solution
    
    """
        Pulls an independent set from the provided subset, by sorting the vertices
        by degree, then greedily adding vertices based on connections to all
        vertices in the set.
    """
    def __greedily_get_ind_subset(self, subset: GraphSubsetTracker) -> set:
        sorted_vertices: [int] = sorted(subset.subset, key= lambda x: subset.internal_degree(x))
        return_value: set = set()

        for node in sorted_vertices:
            # Check if the node connects to anything in the set.
            if count_edge_boundary(self.G, node, return_value) == 0:
                return_value.add(node)
        
        return return_value


    def _run_heuristic(self, intersection_oracle, epsilon):
        #? Set initial solution to empty value
        if self.solution is None:
            self.solution: GraphSubsetTracker = GraphSubsetTracker(self.G, set())
        #? Define inclusion predicate
        def f(v, S: GraphSubsetTracker) -> bool:
            threshold: int = max((S.size() - intersection_oracle(S.subset)) / 2 -  epsilon, 0)
            internal_degree: int = S.internal_degree(v)
            return internal_degree <= threshold
        #? Run successive augmentation
        step: int = 0
        for v in self.G.nodes:
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
            self.solution = GraphSubsetTracker(self.__greedily_get_ind_subset(self.solution))