from typing import Dict, Set, Callable

from graph_coloring.heuristics.graph_coloring_heuristic import GraphColoringHeuristic
from util import graph
from util.models.graph_coloring_tracker import \
    GraphColoringTracker, \
    AVAILABLE_COLORS_AT, \
    UNCOLORED_NODES, \
    NUM_CONFLICTING_EDGES, \
    COLORED_NODES, \
    NUM_NEIGHBORING_COLORS


class BasicLocalSearch(GraphColoringHeuristic):

    def __init__(self):
        super(BasicLocalSearch, self).__init__(expected_metadata_keys=[
            "k",
            'loss_function'
        ])

    def _run_heuristic(self):
        k: int = self.metadata['k']
        loss_function: Callable = self.metadata['loss_function']
        self.solution: GraphColoringTracker = GraphColoringTracker(
            self.G,
            requested_data={
                UNCOLORED_NODES,
                NUM_CONFLICTING_EDGES,
                AVAILABLE_COLORS_AT,
                COLORED_NODES,
                NUM_NEIGHBORING_COLORS
            }
        )

        # Start with a random MAX_DEGREE + delta coloring
        # Note: this is NOT a proper coloring
        partition: Dict[int, Set[int]] = graph.generate_random_color_partition(self.G, k)
        self.solution.set_coloring_with_color_classes(partition)

        # TODO: remove
        assert len(set(self.solution.node_to_color.values())) == k

        i: int = 0
        while True:
            if i % 1000 == 0:
                print(f'[V] On step {i} with {self.solution.num_conflicting_edges} conflicts')
            # improved: bool = False
            conflicts_before = self.solution.num_conflicting_edges

            node, color = self.solution.get_best_move(loss_function)
            old_color = self.solution.node_to_color[node]

            if color == self.solution.node_to_color[node]:
                break
            else:
                self.solution.color_node(node, color)
            i += 1

            assert self.solution.num_conflicting_edges <= conflicts_before

        # Then we're done! Good job team
        return
