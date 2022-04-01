import random
from typing import Callable, List, Set

from networkx.algorithms.similarity import debug_print

from error_correcting_codes.models.algorithms.algorithm import Algorithm
from independent_set.heuristics.independent_set_heuristic import \
    IndependentSetHeuristic
from util.graph import count_edge_boundary
from util.models.graph_subset_tracker import GraphSubsetTracker, get_density
from util.new_graph.models.graph import Graph
from util.new_graph.util import uniformly_sample_subset


class FixedGWW(Algorithm):


    def __init__(self, verbose=False, debug=False, step_hook = None):
        super().__init__(GraphSubsetTracker, verbose, debug)
        self._step_hook = step_hook

    """
        Selects an initial subset uniformly at random from the graph of the
        given size
    """
    def __select_initial_subset(self, size: int) -> GraphSubsetTracker:
        return GraphSubsetTracker(self.G, uniformly_sample_subset(self.G, size))


    """
        Performs a random walk to move the set, where steps is the number of
        random steps to perform (addition / removal of a vertex from the set.)
    """ 
    def __random_walk(self, subset: GraphSubsetTracker, steps: int):
        size: int = subset.size()
        for step in range(steps):
            subset.swap_random_nodes()
        return subset

    
    def _get_best_subset(self, subsets: List[GraphSubsetTracker]) -> Set[int]:
        return min(subsets, key = lambda t: t.num_edges()).subset


    def _clear(self):
        pass


    def _run(self, 
        G: Graph,
        num_particles: Callable, 
        threshold_added_change: int, 
        subset_size: Callable, 
        random_walk_steps: Callable, 
        min_threshold: int,
    ):
        n: int = G.size
        num_particles: int = num_particles(n)
        random_walk_steps: int = random_walk_steps(n)
        subset_size: int = subset_size(n)

        if subset_size > n:
            raise Exception(f"Cannot have subset size {subset_size} > n = {n}")
        if num_particles < 1:
            raise Exception("Cannot run GWW with non-positive number of points")
        if min_threshold < 0:
            raise Exception("Minimum threshold for GWW can not be less than 0.")
        if threshold_added_change > min_threshold:
            raise Exception(f"A threshold density change of {threshold_added_change} will go past 0, as min_threshold is set to {min_threshold} for GWW.")

        subsets: List[GraphSubsetTracker] = [
            self.__select_initial_subset(subset_size) for p in range(num_particles)
        ]

        threshold: float = 0.6

        while threshold > min_threshold:
            new_subsets: List[GraphSubsetTracker] = []
            for subset in subsets:
                if self.__random_walk(subset, random_walk_steps).density() <= threshold:
                    new_subsets.append(subset)

            if len(new_subsets) == 0:
                # No solutions exist under the required threshold
                pass
            
            while len(new_subsets) < num_particles:
                new_subsets.append(random.choice(list(new_subsets)).replicate())
            subsets = new_subsets

            minimum, median, maximum = get_density(subsets)
            threshold = median + threshold_added_change
        
        self._solution: GraphSubsetTracker = self._get_best_subset(subsets)

