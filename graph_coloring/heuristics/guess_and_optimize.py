import copy
import math
from typing import Dict

import networkx as nx

from graph_coloring.heuristics.graph_coloring_heuristic import GraphColoringHeuristic
from util.graph import generate_random_color_partition


class GuessAndOptimize(GraphColoringHeuristic):

    def __init__(self, guess=-1):
        super(GuessAndOptimize, self).__init__()
        self.initial_guess = guess

    def _run_heuristic(self):

        n: int = len(self.G)

        #TODO: do we need stirling table still?

        # Make initial guess
        b: float = 1 / (1 - nx.density(G))
        k: int = self.initial_guess if self.initial_guess != 0 else (n / math.log(n, b))

        # Upper bound phase
        while True:

            # Set the initial solution with a random partitioning into guess # of sets
            self.solution.set_coloring_with_color_classes(generate_random_color_partition(self.G, k))
            if self.solution.get_num_conflicting_edges() == 0 or len(self.solution.color_to_nodes):
                break
            k = k + 1

        # Initialize the above as the best one we have so far.
        best_conflicts: int = self.solution.num_conflicting_edges
        best_labelling: Dict[int, int] = copy.copy(self.solution.node_to_color)

        while True:
            # Try coloring with one less color
            k = k - 1
            # Save old partition
            old_partition: Dict[int, int] = copy.copy(self.solution.node_to_color)
            # TODO: I guess we kinda have to make sure that there's no conflicts...
            self.solution.set_coloring_with_color_classes(generate_random_color_partition(self.G, k))
