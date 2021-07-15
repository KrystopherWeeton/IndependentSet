from util.heuristics.heuristic import Heuristic
from util.models.graph_coloring_tracker import GraphColoringTracker


class GraphColoringHeuristic(Heuristic):

    def __init__(self, expected_metadata_keys: [str] = []):
        super(GraphColoringHeuristic, self).__init__(GraphColoringTracker,
                                                     expected_metadata_keys=expected_metadata_keys)
