import sys
from typing import Callable

from util.graph import count_edge_boundary
from independent_set.heuristics.independent_set_heuristic import IndependentSetHeuristic
from util.models.graph_subset_tracker import GraphSubsetTracker


class SuccessiveAugmentation(IndependentSetHeuristic):

    def __init__(self):
        super().__init__(
            expected_metadata_keys=[
                "K",
                "intersection_oracle",
                "epsilon"
            ]
        )
    
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


    def _run_heuristic(self):
        #? Pull metadata
        N: int = len(self.G.nodes)
        K: int = self.metadata["K"]
        intersection_oracle: Callable = self.metadata["intersection_oracle"]
        epsilon: int = self.metadata["epsilon"]
        #? Metadata validation
        if N <= 0 or K <= 0 or K > N:
            print(f"ERROR: Unable to run heuristic with metadata provided. N={N}, K={K}")
            sys.exit(1)
        #? Set initial solution to empty value
        #self.solution: GraphSubsetTracker = GraphSubsetTracker(self.G)

        #? Define inclusion predicate
        def f(v, S: GraphSubsetTracker) -> bool:
            m: int = S.size()
            threshold: int = (m - intersection_oracle(S.subset)) / 2 -  epsilon
            if threshold < 0:
                threshold = 0
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