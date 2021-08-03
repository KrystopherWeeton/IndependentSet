from typing import Dict, Set

from graph_coloring.heuristics.graph_coloring_heuristic import GraphColoringHeuristic
from util import graph
from util.graph import max_degree
from util.models.graph_coloring_tracker import \
    GraphColoringTracker, \
    AVAILABLE_COLORS_AT, \
    UNCOLORED_NODES, \
    NUM_CONFLICTING_EDGES, \
    COLORED_NODES, \
    NUM_NEIGHBORING_COLORS


class GlauberDynamics(GraphColoringHeuristic):

    def __init__(self):
        super(GlauberDynamics, self).__init__(expected_metadata_keys=[
            "delta",
            "max_iterations"
        ])

    def _run_heuristic(self, delta, max_iterations):
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

        k: int = min(max_degree(self.G) + delta, len(self.G))

        # Start with a random MAX_DEGREE + delta coloring
        # Note: this is NOT a proper coloring
        partition: Dict[int, Set[int]] = graph.generate_random_color_partition(self.G, k)
        self.solution.set_coloring_with_color_classes(partition)

        # TODO: remove
        assert len(set(self.solution.node_to_color.values())) == k

        # Just keep recoloring until we get to a proper coloring
        while (
                (not self.solution.is_proper() and self.solution.is_complete()) and
                self.solution.calls_to_color_node < max_iterations
        ):

            conflicts_before = self.solution.num_conflicting_edges

            # if self.solution.calls_to_color_node % 1000 == 0:
            # print(f'Trying to recolor a node at iteration {self.solution.calls_to_color_node}')
            # print(f'Current Conflicts: {self.solution.num_conflicting_edges}')

            # Get a random node
            node = self.solution.get_random_node()

            # and color it a random AVAILABLE color (but only if we can
            if len(self.solution.available_colors_at[node]) == 0:
                pass
                # print(f'Couldn\'t recolor a node at iteration {self.solution.calls_to_color_node}')
            else:
                self.solution.color_node(node, self.solution.get_random_available_color(node))

            assert self.solution.num_conflicting_edges <= conflicts_before

        # Then we're done! Good job team
        return
