import random
from typing import List

from networkx.algorithms.similarity import debug_print

from independent_set.heuristics.independent_set_heuristic import \
    IndependentSetHeuristic
from util.graph import count_edge_boundary
from util.models.graph_subset_tracker import GraphSubsetTracker, get_density
from util.new_graph.util import uniformly_sample_subset

# This is a comment

class FixedGWW(IndependentSetHeuristic):

    def __init__(self, verbose: bool = False, debug: bool = False):
        super().__init__(
            expected_metadata_keys=[
                "num_particles",
                "threshold_added_change",
                "subset_size",
                "random_walk_steps",
                "min_threshold",
            ],
            verbose=verbose,
            debug=debug
        )


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

    
    def _get_best_subset(self, subsets: List[GraphSubsetTracker]) -> set:
        return min(subsets, key = lambda t: t.num_edges()).subset

    def _run_heuristic(self, num_particles, threshold_added_change, subset_size, random_walk_steps, min_threshold):
        n: int = self.G.size
        num_particles: int = num_particles(n)
        random_walk_steps: int = random_walk_steps(n)
        subset_size: int = subset_size(n)

        self.verbose_print([
                f"Running heuristic with the following arguments",
                f"Num. Particles: {num_particles}",
                f"Random Walk Steps: {random_walk_steps}",
                f"Subset Size: {subset_size}",
                f"[V] ==========="
        ])

        #? Metadata validation
        if subset_size > n:
            self.verbose_print(f"Running fixed gww with subset size too large ({subset_size} > {n}). Returning empty set")
            self.solution = set()
            return

        if num_particles < 1:
            raise Exception("Cannot run GWW with non-positive number of points")
        
        if min_threshold < 0:
            raise Exception("Minimum threshold for GWW can not be less than 0.")

        if threshold_added_change > min_threshold:
            raise Exception(f"A threshold density change of {threshold_added_change} will go past 0, as min_threshold is set to {min_threshold} for GWW.")


        #? Initialize trackers
        # The point trackers
        subsets: List[GraphSubsetTracker] = [ 
            self.__select_initial_subset(subset_size) for p in range(num_particles)
        ]
        # The threshold that all points should satisfy
        threshold: float = 0.6

        while threshold > min_threshold:
            debug_print(f"Threshold: {threshold}")
            #? Take a random walk at each point
            for subset in subsets:
                self.__random_walk(subset, random_walk_steps)

            #? Remove all subsets which are not below the threshold
            temp_subsets = [
                subset for subset in subsets if subset.density() <= threshold
            ]

            #? Replicate subsets until points are replenished
            debug_print(f"{len(temp_subsets)} / {num_particles} surviving particles.")

            # Check if subsets is empty
            if len(temp_subsets) == 0:
                self.solution = self._get_best_subset(subsets)
                self.verbose_print(f"WARNING: Unable to replicate points because no subsets survived.")
                return
            while len(temp_subsets) < num_particles:
                temp_subsets.append(random.choice(list(temp_subsets)).replicate())
            subsets = temp_subsets


            #? Reduce the threshold for next iteration
            minimum, median, maximum = get_density(subsets)
            threshold = median + threshold_added_change
        
        #? Greedily pull largest independent set from each subset, then
        #? return the largest independent set found.
        self.solution = self._get_best_subset(subsets)


TESTING_METADATA_FIXED_GWW: dict = {
    "num_particles":            lambda n: 30,
    "subset_size":              30,
    "thresold_added_change":    0.01,
    "random_walk_steps":        lambda n: 30,
    "min_threshold":            0.1,
}
