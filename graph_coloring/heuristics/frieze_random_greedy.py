import copy
import random
random.seed(1)

from graph_coloring.heuristics.graph_coloring_heuristic import GraphColoringHeuristic
from util.models.graph_coloring_tracker import GraphColoringTracker


class FriezeRandomGreedy(GraphColoringHeuristic):

    def __init__(self):
        # Frieze Random Greedy doesn't really need anything
        super(FriezeRandomGreedy, self).__init__()

    def _run_heuristic(self):

        self.solution: GraphColoringTracker = GraphColoringTracker(self.G)

        k: int = 0
        # Make independent sets
        while len(self.solution.get_uncolored_nodes()) != 0:

            ind_set: set = copy.copy(self.solution.get_uncolored_nodes())

            while len(ind_set) != 0:
                v: int = random.choice(list(ind_set))
                ind_set.remove(v)

                self.solution.color_node(node=v, color=k)

                ind_set = ind_set.difference(set(self.G[v]))
            k += 1
