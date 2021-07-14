import copy

from util.heuristics.heuristic import Heuristic, SeededHeuristic
from util.models.graph_subset_tracker import GraphSubsetTracker

class PhaseHeuristic(Heuristic):


    def __init__(self, *argv: [Heuristic]):
        super(
            expected_metadata_keys = ["metadata"]
        )
        self.heuristics: [Heuristic] = argv

    
    def _run_heuristic(self):
        """
            Runs h1, then passes whatever h1 finds as a solution to h2
        """
        metadata: [dict] = self.metadata["metadata"]
        
        if len(metadata) != len(self.heuristics):
            raise RuntimeError("Phase heuristics was run with invalid length of metadata.")

        for i, h in enumerate(self.heuristics):
            h.run_heuristic(self.G, metadata[i], self.solution) # Note: self.solution is a shallow copy, so solution subset is same throughout.