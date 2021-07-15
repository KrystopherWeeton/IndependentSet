import random
from typing import Callable

import networkx as nx
import numpy as np

from util.graph import count_edge_boundary
from util.heuristics.graph_subset_tracker import (GraphSubsetTracker,
                                                  create_graph_subset_tracker,
                                                  get_density)
from util.heuristics.heuristic import Heuristic


class GWW(Heuristic):


    def __init__(self):
        super().__init__(
            expected_metadata_keys=[
                "num_particles", 
                "min_subset_size", 
                "threshold_added_change",
                "random_walk_steps",
                "min_threshold",
                "verbose",
            ]
        )


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
    def __random_walk(self, subset: GraphSubsetTracker, steps: int, min_size: int) -> set:
        size: int = subset.size()

        for step in range(steps):
            if size == min_size:
                subset.add_random_node()
                size += 1
            elif size == len(self.G.nodes):
                subset.remove_random_node()
                size -= 1
            else:
                if random.randint(0, 1):
                    subset.add_random_node()
                    size += 1
                else:
                    subset.remove_random_node()
                    size -= 1
        return subset

    
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

    def __get_best_subset(self, subsets: [GraphSubsetTracker]) -> GraphSubsetTracker:
        return min(subsets, lambda t: t.num_edges())

    def _run_heuristic(self):
        #? Pull metadata
        n: int = len(self.G.nodes)
        num_particles: int = self.metadata["num_particles"](n)
        random_walk_steps: int = self.metadata["random_walk_steps"](n)
        min_subset_size: int = self.metadata["min_subset_size"]
        threshold_added_change: float = self.metadata["threshold_added_change"]
        min_threshold: float = self.metadata["min_threshold"]
        verbose: bool = self.metadata["verbose"]

        if verbose:
            print(f"Received metadata: {self.metadata}. Running with {num_particles} particles.")

        #? Metadata validation
        if num_particles < 1:
            raise Exception("Cannot run GWW with non-positive number of points")
        
        if min_threshold < 0:
            raise Exception("Minimum threshold for GWW can not be less than 0.")

        if threshold_added_change > min_threshold:
            raise Exception(f"A threshold density change of {threshold_added_change} will go past 0, as min_threshold is set to {min_threshold} for GWW.")


        #? Initialize trackers
        # The point trackers
        subsets: [GraphSubsetTracker] = [ 
            self.__select_initial_subset(min_subset_size) for p in range(num_particles)
        ]
        # The threshold that all points should satisfy
        threshold: float = 0.6

        while threshold > min_threshold:
            if verbose:
                print(f"Running iteration with threshold {threshold}.")
            #? Take a random walk at each point
            for subset in subsets:
                self.__random_walk(subset, random_walk_steps, min_subset_size)

            #? Remove all subsets which are not below the threshold
            temp_subsets = [
                subset for subset in subsets if subset.density() <= threshold
            ]

            #? Replicate subsets until points are replenished
            if verbose:
                print(f"Number of subsets after removal is {len(temp_subsets)}.")
            
            # Check if subsets is empty
            if len(temp_subsets) == 0:
                self.solution = self.__get_best_subset(subsets)
                print(f"WARNING: Unable to replicate points because no subsets survived.")
                return
            while len(temp_subsets) < num_particles:
                temp_subsets.append(random.choice(list(temp_subsets)).replicate())
            subsets = temp_subsets


            #? Reduce the threshold for next iteration
            minimum, median, maximum = get_density(subsets)
            threshold = median - threshold_added_change
        
        #? Greedily pull largest independent set from each subset, then
        #? return the largest independent set found.
        self.solution = self.__get_best_subset(subsets)


TESTING_METADATA_GWW: dict = {
    "num_particles":               lambda n: 30,
    "min_subset_size":          30,
    "threshold_density_change": 0.025,
    "random_walk_steps":        lambda n: 30,
    "min_threshold":            0.1,
    "verbose":                  False,
}