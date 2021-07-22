from graph_coloring.heuristics.graph_coloring_heuristic import GraphColoringHeuristic

from util.graph import generate_random_color_partition


class GlauberDynamics(GraphColoringHeuristic):

    def __init__(self):
        super(GlauberDynamics, self).__init__(expected_metadata_keys=[
            "delta"
        ])

    def _run_heuristic(self):
        delta: int = self.metadata["delta"]

        # Start with a random MAX_DEGREE + delta coloring
        # Note: this is NOT a proper coloring
        self.solution.set_coloring_with_color_classes(generate_random_color_partition(self.G, self.G.degree + delta))

        # Just keep recoloring until we get to a proper coloring
        while not self.solution.is_proper_and_complete():
            self.solution.recolor_random_node_a_random_color()

        # Then we're done! Good job team
        return
