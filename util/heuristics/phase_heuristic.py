from util.heuristics.heuristic import Heuristic, SeededHeuristic
from util.models.graph_subset_tracker import GraphSubsetTracker

import copy



class PhaseHeuristic(Heuristic):


    def __init__(self, h1: Heuristic, h2: SeededHeuristic):
        super(
            expected_metadata_keys = [
                "h1_metadata", "h2_metadata"
            ]
        )
        self.h1 = h1
        self.h2 = h2

    
    def _run_heuristic(self):
        """
            Runs h1, then passes whatever h1 finds as a solution to h2
        """
        self.h1.run_heuristic(self.G, self.metadata["h1_metadata"])
        solution: set = self.h1.solution.subset

        self.h2.run_heuristic(self.G, solution, self.metadata["h2_metadata"])
        pass