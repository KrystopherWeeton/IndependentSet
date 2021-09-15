import copy
import random
import sys
from typing import Callable, List, Set

from independent_set.heuristics.independent_set_heuristic import \
    IndependentSetHeuristic
from independent_set.heuristics.successive_augmentation import \
    SuccessiveAugmentation
from util.models.graph_subset_tracker import GraphSubsetTracker
from util.new_graph.util import greedily_recover_ind_subset


class RepeatedSuccessiveAugmentation(IndependentSetHeuristic):
    def __init__(
        self,
        max_iterations: int,
        init_epsilon: int,
        next_epsilon: int,
        verbose: bool = False,
        debug: bool = False,
    ):
        super().__init__(
            expected_metadata_keys=[
                "intersection_oracle",
            ],
            verbose=verbose,
            debug=debug,
        )
        self.max_iterations: int = max_iterations
        self.init_epsilon: int = init_epsilon
        self.next_epsilon: int = next_epsilon
        self.successive_augmentation: SuccessiveAugmentation = SuccessiveAugmentation(
            True, verbose, debug
        )

    def _run_heuristic(self, intersection_oracle: Callable):
        assert (
            self.solution is not None
        ), "Repeated successive augmentaiton requires a seed set"
        self.node_list = self.G.vertex_list()

        completed_iterations: int = 0
        epsilon: int = self.init_epsilon
        while completed_iterations < self.max_iterations:
            # * Clear and run successive augmentation
            self.successive_augmentation.clear()
            self.successive_augmentation.run_heuristic(
                self.G,
                {"intersection_oracle": intersection_oracle, "epsilon": epsilon},
                seed=self.solution,
            )
            self.solution = self.successive_augmentation.solution
            # * Call post_step_hook
            self.call_post_step_hook(self.solution, completed_iterations)
            # * Update and prepare for next iteration
            epsilon = self.next_epsilon(epsilon)
            completed_iterations += 1
