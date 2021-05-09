import networkx as nx
import numpy as np
from typing import Callable

from util.heuristics.heuristic import Heuristic
import random
import json
from util.heuristics.graph_subset_tracker import GraphSubsetTracker, create_graph_subset_tracker, get_density
from util.local_optimization.swap_purge import SwapPurgeLocalOptimizer
from util.local_optimization.local_optimization import LocalOptimizer
from util.graph import count_edge_boundary


class FixedGWW(Heuristic):


    def __init__(self):
        super().__init__(
            expected_metadata_keys=[
                "num_particles", 
                "threshold_added_change",
                "subset_size",
                "random_walk_steps",
                "min_threshold",
                "verbose",
            ]
        )
        self.optimizer: LocalOptimizer = SwapPurgeLocalOptimizer(1)


    """
        Selects an initial subset uniformly at random from the graph of the
        given size
    """
    def __select_initial_subset(self, size: int) -> GraphSubsetTracker:
        subset = set(random.sample(list(self.G.nodes), size))
        return create_graph_subset_tracker(self.G, subset)


    """
        Performs a random walk to move the set, where steps is the number of
        random steps to perform (addition / removal of a vertex from the set.)
    """ 
    def __random_walk(self, subset: GraphSubsetTracker, steps: int):
        size: int = subset.size()
        for step in range(steps):
            subset.swap_random_nodes()

    
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



    """
        Runs a local optimizer from the provided headstart_set. Returns the result as a
        set of nodes.
    """
    def __run_local_optimizer(self, headstart_set: GraphSubsetTracker) -> set:
        self.optimizer.clear()
        return self.optimizer.optimize(headstart_set.subset, self.G, 9999)


    def __get_best_ind_set(self, subsets: [GraphSubsetTracker]) -> GraphSubsetTracker:
        subsets = [
            self.__greedily_get_ind_subset(create_graph_subset_tracker(self.G, self.__run_local_optimizer(subset)))
                 for subset in subsets
        ]
        return create_graph_subset_tracker(self.G, subsets[np.argmax([len(x) for x in subsets])])


    def _run_heuristic(self):
        #? Pull metadata
        n: int = len(self.G.nodes)
        num_particles: int = self.metadata["num_particles"](n)
        random_walk_steps: int = self.metadata["random_walk_steps"](n)
        subset_size: int = self.metadata["subset_size"](n)
        threshold_added_change: float = self.metadata["threshold_added_change"]
        min_threshold: float = self.metadata["min_threshold"]
        verbose: bool = self.metadata["verbose"]

        if verbose:
            print(
                f"[V] Running Heuristic with the following arguments\n"
                f"[V] Number of Particles: {num_particles}\n"
                f"[V] Random Walk Steps: {random_walk_steps}\n"
                f"[V] Subset Size: {subset_size}\n"
                f"[V] ==========="
            )

        #? Metadata validation
        if subset_size > n:
            if verbose:
                print(
                    f"[V] Running fixed gww with subset size too large ({subset_size} > {n}). Returning empty set."
                )
                self.solution = create_graph_subset_tracker(self.G, set())
                return

        if num_particles < 1:
            raise Exception("Cannot run GWW with non-positive number of points")
        
        if min_threshold < 0:
            raise Exception("Minimum threshold for GWW can not be less than 0.")

        if threshold_added_change > min_threshold:
            raise Exception(f"A threshold density change of {threshold_added_change} will go past 0, as min_threshold is set to {min_threshold} for GWW.")


        #? Initialize trackers
        # The point trackers
        subsets: [GraphSubsetTracker] = [ 
            self.__select_initial_subset(subset_size) for p in range(num_particles)
        ]
        # The threshold that all points should satisfy
        threshold: float = 0.6

        while threshold > min_threshold:
            #if verbose:
            #    print(f"[V] Threshold: {threshold}.")
            #? Take a random walk at each point
            for subset in subsets:
                self.__random_walk(subset, random_walk_steps)

            #? Remove all subsets which are not below the threshold
            temp_subsets = [
                subset for subset in subsets if subset.density() <= threshold
            ]

            #? Replicate subsets until points are replenished
            #if verbose:
            #    print(f"[V] {len(temp_subsets)} / {num_particles} surviving particles.")
            
            # Check if subsets is empty
            if len(temp_subsets) == 0:
                self.solution = self.__get_best_ind_set(subsets)
                print(f"WARNING: Unable to replicate points because no subsets survived.")
                return
            while len(temp_subsets) < num_particles:
                temp_subsets.append(random.choice(list(temp_subsets)).replicate())
            subsets = temp_subsets


            #? Reduce the threshold for next iteration
            minimum, median, maximum = get_density(subsets)
            threshold = median + threshold_added_change
        
        #? Greedily pull largest independent set from each subset, then
        #? return the largest independent set found.
        self.solution = self.__get_best_ind_set(subsets)


TESTING_METADATA_FIXED_GWW: dict = {
    "num_particles":            lambda n: 30,
    "subset_size":              30,
    "thresold_added_change":    0.01,
    "random_walk_steps":        lambda n: 30,
    "min_threshold":            0.1,
    "verbose":                  False,
}