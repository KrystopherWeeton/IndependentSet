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

        self.solution: GraphColoringTracker = GraphColoringTracker(
            self.G,
            requested_data={'uncolored_nodes'}
        )

        k: int = 0
        # Make independent sets
        while len(self.solution.get_uncolored_nodes()) != 0:
            print(f'[V]: Making {k}th color class')

            ind_set: set = copy.copy(self.solution.get_uncolored_nodes())

            num_added: int = 0
            while len(ind_set) != 0:
                num_added += 1
                v: int = random.choice(list(ind_set))
                ind_set.remove(v)

                self.solution.color_node(node=v, color=k)

                ind_set = ind_set.difference(set(self.G[v]))
            print(f'[V] Was able to make a color class of size {num_added}.')
            k += 1
