import sys
from typing import Callable

from util.graph import count_edge_boundary
from independent_set.heuristics.independent_set_heuristic import IndependentSetHeuristic
from util.models.graph_subset_tracker import GraphSubsetTracker
from util.misc import validate


class RepeatedSuccessiveAugmentation(IndependentSetHeuristic):
    """
        METADATA
            :param: intersection_oracle - A required oracle providing the intersection of a subset with the planted
            :param: epsilons - The 'extra' requirement for degree for inclusion, list of values for each repetition
            :param: num_repetitions - The number of times to repeat successive augmentation
    """

    def __init__(self):
        super().__init__(
            expected_metadata_keys=[
                "intersection_oracle",
                "epsilons",
                "num_repetitions"
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
    
    def __run_suc_aug(self, inclusion_predicate: Callable, step: int) -> GraphSubsetTracker:
        #? Run successive augmentation
        for v in self.G.nodes:
            if v in self.solution.subset:
                continue
            # Determine whether or not to include v
            include_v = inclusion_predicate(v, self.solution)
            if include_v:
                self.solution.add_node(v)
            
            #? Update results
            self.call_post_step_hook(self.solution.subset, step)
            step += 1
        return step


    def _run_heuristic(self):
        #? Pull metadata
        N: int = len(self.G.nodes)
        intersection_oracle: Callable = self.metadata["intersection_oracle"]
        num_repetitions: int = self.metadata["num_repetitions"]
        epsilons: [int] = self.metadata["epsilons"]
        #? Set initial solution to empty value
        self.solution: GraphSubsetTracker = GraphSubsetTracker(self.G)

        validate(num_repetitions == len(epsilons), f"{num_repetitions} repetitions cannot be used with only {len(epsilons)} epsilons provided.")

        step: int = 0
        for i in range(num_repetitions):
            def f(v, S: GraphSubsetTracker) -> bool:
                threshold: int = max(0, (S.size() - intersection_oracle(S.subset)) / 2 - epsilons[i])
                return S.internal_degree(v) <= threshold
            
            step = self.__run_suc_aug(f, step)