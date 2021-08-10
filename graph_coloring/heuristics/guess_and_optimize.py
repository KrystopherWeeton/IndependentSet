import copy
import math
from typing import Dict

import networkx as nx

from graph_coloring.heuristics.graph_coloring_heuristic import GraphColoringHeuristic
from util.graph import generate_random_color_partition
from util.models.graph_coloring_tracker import GraphColoringTracker


class GuessAndOptimize(GraphColoringHeuristic):

    def __init__(self, guess=-1):
        super(GuessAndOptimize, self).__init__([
            "initial_guess",
            "optimization_function"
        ])
        self.initial_guess = guess

    def _optimize(self, iterations: int):
        for i in range(iterations):
            if self.verbose and ((i * 100) / iterations) % 10 == 0:
                print(f'[V] Iteration: {i}, Current Conflicting Edges: {self.solution.num_conflicting_edges}')

            # Find the most conflicted node
            most_conflicted: int = self.solution.most_collisions_node()

            # Recolor this node
            self.solution.color_node(most_conflicted, self.solution.best_recoloring(most_conflicted))

    def _run_heuristic(self):

        n: int = len(self.G)
        self.solution: GraphColoringTracker = GraphColoringTracker(self.G)

        # TODO: do we need stirling table still?

        # Make initial guess
        # TODO: Check out density condition here
        b: float = 1 / (1 - nx.density(self.G))
        k: int = self.initial_guess if self.initial_guess > 0 else round(n / math.log(n, b))
        iterations: int = n * k * 10
        tries: int = n

        # Upper bound phase
        while True:
            if self.verbose:
                print(f'[V] Testing coloring with {k} colors')
            # Set the initial solution with a random partitioning into guess # of sets
            self.solution.set_coloring_with_color_classes(generate_random_color_partition(self.G, k))
            # Now try to optimize for iterations
            self._optimize(iterations)
            # If we got to a valid solution, don't need to go up any more
            if (
                    self.solution.get_num_conflicting_edges() == 0 or
                    len(self.solution.color_to_nodes) == len(self.G) or
                    k >= len(self.G)
            ):
                break
            k = k + 1

        # Initialize the above as the best one we have so far.

        while True:
            # Question: Do we need to know the conflict here? Could be interesting if we could do
            best_conflicts: int = self.solution.num_conflicting_edges
            best_labelling: Dict[int, int] = copy.copy(self.solution.node_to_color)

            # Try coloring with one less color
            k = k - 1
            self.solution.set_coloring_with_color_classes(generate_random_color_partition(self.G, k))

            self._optimize(iterations)

            # If we ran into conflicts on this one, lets just revert back to the last one.
            if self.solution.get_num_conflicting_edges() != 0:
                self.solution.set_coloring_with_node_labels(best_labelling)
                break

        return
