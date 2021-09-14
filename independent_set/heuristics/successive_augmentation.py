import random
from typing import List

from independent_set.heuristics.independent_set_heuristic import \
    IndependentSetHeuristic
from util.graph import count_edge_boundary
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
                "epsilon",
                "restart_threshold",
                "restart_checkpoint",
                "restarts_allowed"
            ],
            verbose=verbose,
            debug=debug
        )
        self.prune_final_solution: bool = prune_final_solution
        self.permute_vertices: bool = permute_vertices
    
    """
        Pulls an independent set from the provided subset, by sorting the vertices
        by degree, then greedily adding vertices based on connections to all
        vertices in the set.
    """

    def __greedily_get_ind_subset(self, subset: GraphSubsetTracker) -> set:
        sorted_vertices: List[int] = sorted(subset.subset, key=lambda x: subset.internal_degree(x))
        return_value: set = set()

        for node in sorted_vertices:
            # Check if the node connects to anything in the set.
            if count_edge_boundary(self.G, node, return_value) == 0:
                return_value.add(node)

        return return_value

    def _reset(self):
        # ? Do we want to restart from beginning or restart from the "headstart" if it was given?
        if self.solution is None:
            self.solution: GraphSubsetTracker = GraphSubsetTracker(self.G, set())

    def _run_heuristic(self, intersection_oracle, epsilon, restart_threshold, restart_checkpoint, restarts_allowed):
        # ? Set initial solution to empty value
        if self.solution is None:
            self.solution: GraphSubsetTracker = GraphSubsetTracker(self.G, set())

        # ? Define inclusion predicate
        def f(v, S: GraphSubsetTracker) -> bool:
            threshold: int = max((S.size() - intersection_oracle(S.subset)) / 2 - epsilon, 0)
            internal_degree: int = S.internal_degree(v)
            return internal_degree <= threshold

        # Generate node list and permute if appropriate
        self.node_list: List[int] = list(self.G.nodes)
        if self.permute_vertices:
            random.shuffle(self.node_list)
        # ? Run successive augmentation
        step: int = 0
        restarts: int = 0
        i: int = 0
        while i < len(self.node_list):
            # If we get to the restart checkpoint, and we're not doing better than the restart threshold, repermute the
            # vertices and start over.
            if restarts < restarts_allowed and i == restart_checkpoint and restart_threshold < self.solution.density():
                random.shuffle(self.node_list)
                i = 0
                restarts += 1
                self._reset()
            v = self.node_list[i]
            if v in self.solution.subset:
                continue
            # Determine whether or not to include v
            include_v = f(v, self.solution)
            if include_v:
                self.solution.add_node(v)

            # ? Update results
            self.call_post_step_hook(self.solution.subset, step)
            step += 1
        #? Prune final solution if required 
        if self.prune_final_solution:
            self.solution = GraphSubsetTracker(self.G, self.__greedily_get_ind_subset(self.solution))
