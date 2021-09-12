import math
import random

import util.formulas as formulas
from independent_set.heuristics.independent_set_heuristic import \
    IndependentSetHeuristic
from util.models.graph_subset_tracker import GraphSubsetTracker


class Metropolis(IndependentSetHeuristic):

    def __init__(self, verbose: bool = False, debug: bool = False):
        super().__init__(expected_metadata_keys=["temperature", "max_steps"], verbose=verbose, debug=debug)

    """
        Calculates the threshold when presented with an option that increases density
    """

    def __calc_threshold(self, density: float, temperature: float) -> float:
        threshold = math.e ** (-density / temperature)
        if threshold > 1:
            raise Exception(f"Metropolis got a threshold {threshold} > 1.")
        return threshold


    def __select_initial_subset(self):
        # Right now just select a random point
        x = random.choice(self.G.vertex_list())
        return set([x])


    def _run_heuristic(self, temperature, max_steps):
        # Set initial solution to initial subset selected
        solution: GraphSubsetTracker = self.__select_initial_subset()

        # Perform actual metropolis process
        for i in range(max_steps):
            k: int = solution.size()

            #? Generate a candidate and calculate new density
            node: int = random.choice(self.G.vertex_list())
            removing: bool = node in solution
            internal_degree: int = solution.internal_degree(node)
            if removing:
                new_density: float = formulas.density_after_rem(solution.density(), k, internal_degree)
            else:
                new_density: float = formulas.density_after_add(solution.density(), k, internal_degree)

            #? Calculate acceptance threshold, determine action
            threshold: float = self.__calc_threshold(new_density, temperature)
            if random.random() <= threshold:
                if removing:
                    solution.remove_node(node)
                else:
                    solution.add_node(node)

        # Ran out of steps. Give warning then bail
        self.verbose_print(
            f"Warning: Metropolis ran {max_steps} without terminating."
        )
        self.solution = solution.subset


TESTING_METADATA: dict = {
    "temperature": 0.5,
    "max_steps": 999
}
