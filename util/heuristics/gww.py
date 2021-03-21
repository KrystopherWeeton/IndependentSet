import networkx as nx
import numpy as np

from util.heuristics.heuristic import Heuristic
import random
from util.heuristics.graph_subset_tracker import GraphSubsetTracker


class GWW(Heuristic):


    def __init__(self):
        super().__init__(
            expected_metadata_keys=[
                "num_points", 
                "min_subset_size", 
                "threshold_density_change",
                "random_walk_steps",
                "min_threshold",
            ]
        )


    """
        Selects an initial subset uniformly at random from the graph of the
        given size
    """
    def __select_initial_subset(self, size: int) -> GraphSubsetTracker:
        subset = set(random.sample(list(self.G.nodes), size))
        return GraphSubsetTracker(self.G, subset)


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
            if len(nx.edge_boundary(self.G, set(node), return_value)) == 0:
                return_value.add(node)
        
        return return_value




    def _run_heuristic(self):
        #? Pull metadata
        num_points: int = self.metadata["num_points"]
        min_subset_size: int = self.metadata["min_subset_size"]
        threshold_density_change: float = self.metadata["threshold_density_change"]
        random_walk_steps: int = self.metadata["random_walk_steps"]
        min_threshold: float = self.metadata["min_threshold"]

        #? Metadata validation
        if num_points < 1:
            raise Exception("Cannot run GWW with non-positive number of points")
        
        if min_threshold < 0:
            raise Exception("Minimum threshold for GWW can not be less than 0.")

        if threshold_density_change > min_threshold:
            raise Exception(f"A threshold density change of {threshold_density_change} will go past 0, as min_threshold is set to {min_threshold} for GWW.")


        #? Initialize trackers
        # The point trackers
        subsets: [GraphSubsetTracker] = [ 
            self.__select_initial_subset(min_subset_size) for p in range(num_points)
        ]
        # The threshold that all points should satisfy
        threshold: float = 1

        while threshold > min_threshold:
            #? Take a random walk at each point
            for subset in subsets:
                self.__random_walk(subset, random_walk_steps, min_subset_size)

            #? Remove all subsets which are not below the threshold
            subsets = [
                subset for subset in subsets if subset.density() <= threshold
            ]

            #? Replicate subsets until points are replenished
            while len(subsets) < num_points:
                subsets.append(random.choice(self.subsets).replicate())


            #? Reduce the threshold for next iteration
            threshold -= threshold_density_change
        
        #? Greedily pull largest independent set from each subset, then
        #? return the largest independent set found.
        subsets: [ set ] = [
            self.__greedily_get_ind_subset(subset) for subset in subsets
        ]
        return subsets[np.argmax([len(x) for x in subsets])]