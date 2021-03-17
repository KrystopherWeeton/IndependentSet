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
                "random_walk_steps"
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


    def _run_heuristic(self):
        #? Pull metadata
        num_points: int = self.metadata["num_points"]
        min_subset_size: int = self.metadata["min_subset_size"]
        threshold_density_change: float = self.metadata["threshold_density_change"]
        random_walk_steps: int = self.metadata["random_walk_steps"]


        #? Initialize trackers
        # The point trackers
        subsets: [GraphSubsetTracker] = [ 
            self.__select_initial_subset(min_subset_size) for p in range(num_points)
        ]
        # The threshold that all points should satisfy
        threshold: float = 1

        # TODO: When do I stop?????
        while True:
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