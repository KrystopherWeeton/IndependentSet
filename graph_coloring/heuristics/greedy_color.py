import copy
import random

from graph_coloring.heuristics.graph_coloring_heuristic import GraphColoringHeuristic
from util.models.graph_coloring_tracker import \
    GraphColoringTracker, \
    AVAILABLE_COLORS_AT, \
    UNCOLORED_NODES, \
    NUM_CONFLICTING_EDGES, \
    COLORED_NODES, \
    NUM_NEIGHBORING_COLORS, \
    SATURATION

greedy_strategies = {
    'random',
    'DSatur'
}

class GreedyColor(GraphColoringHeuristic):

    def __init__(self):
        # Frieze Random Greedy doesn't really need anything
        super(GreedyColor, self).__init__(expected_metadata_keys=[
            'greedy_strategy'
        ])

    def _random_greedy(self):
        k: int = 0
        # Make independent sets
        while len(self.solution.get_uncolored_nodes()) != 0:
            # print(f'[V]: Making {k}th color class')

            ind_set: set = copy.copy(self.solution.get_uncolored_nodes())

            num_added: int = 0
            while len(ind_set) != 0:
                num_added += 1

                v: int = random.choice(list(ind_set))
                ind_set.remove(v)

                # Now color the node according to the right greedy strategy
                color: int = k

                self.solution.color_node(node=v, color=color)

                ind_set = ind_set.difference(set(self.G[v]))
            # print(f'[V] Was able to make a color class of size {num_added}.')
            k += 1

    def _DSatur(self):
        while len(self.solution.get_uncolored_nodes()) != 0:
            v: int = self.solution.pop_most_saturated_node()
            color: int = self.solution.get_random_available_color(v, True)
            self.solution.color_node(node=v, color=color)

    def _run_heuristic(self, greedy_strategy: str):

        requested_data = {'uncolored_nodes'}
        if greedy_strategy == 'DSatur':
            requested_data = requested_data.union({
                UNCOLORED_NODES,
                NUM_CONFLICTING_EDGES,
                AVAILABLE_COLORS_AT,
                COLORED_NODES,
                NUM_NEIGHBORING_COLORS,
                SATURATION
            })

        self.solution: GraphColoringTracker = GraphColoringTracker(
            self.G,
            requested_data=requested_data
        )

        if greedy_strategy not in greedy_strategies:
            raise AttributeError(f'{greedy_strategy} is not implemented')

        # greedy_node_selection, greedy_coloring_selection = {
        #     'DSatur': (self.solution.get_most_saturated_node, self.solution.get_random_available_color),
        #     'random': (self.solution.get_random_node, self.solution.get_random_available_color)
        # }[greedy_strategy]
        if greedy_strategy == 'random':
            self._random_greedy()
        elif greedy_strategy == 'DSatur':
            self._DSatur()
