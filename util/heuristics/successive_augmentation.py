from util.heuristics.heuristic import Heuristic
from util.results.sa_results import SuccAugResults
from util.models.graph_subset_tracker import GraphSubsetTracker
from util.graph import count_edge_boundary
from util.formulas import subsets
from typing import Callable
import math
import sys


class SuccessiveAugmentation(Heuristic):

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

        #? Define inclusion predicate
        def f(v, S: GraphSubsetTracker) -> bool:
            m: int = S.size()
            #! Somewhere near expectation?
            #threshold: int = (math.sqrt(m) * (math.sqrt(m) - 1)) / 2
            #! Oracle call here. Not realistic!
            # threshold: int = (m - intersection_oracle(S.subset)) / 2 - 3
            threshold: int = (m - intersection_oracle(S.subset)) / epsilon
            if threshold < 0:
                threshold = 0
            internal_degree: int = S.internal_degree(v)
            return internal_degree <= threshold

        #? Run successive augmentation
        subset: GraphSubsetTracker = self.solution
        step: int = 0
        for v in self.G.nodes:
            if v in subset.subset:
                continue
            # Determine whether or not to include v
            include_v = f(v, subset)
            if include_v:
                subset.add_node(v)
            
            #? Update results
            self.call_post_step_hook(subset.subset, step)
            step += 1

        #? Prune to get a final solution
        #! Stop pruning for now. We can add this back in.
        #self.solution = create_graph_subset_tracker(self.G, self.__greedily_get_ind_subset(subset))
        self.solution = subset



