from typing import List

from independent_set.heuristics.independent_set_heuristic import \
    IndependentSetHeuristic
from util.models.graph_subset_tracker import GraphSubsetTracker


class PhaseHeuristic(IndependentSetHeuristic):

    def __init__(self, *argv: List[IndependentSetHeuristic], verbose: bool = False, debug: bool = False):
        super().__init__(expected_metadata_keys=["metadata"], verbose=verbose, debug=debug)
        self.heuristics: List[IndependentSetHeuristic] = argv

    def _run_heuristic(self, metadata):
        """
            Runs h1, then passes whatever h1 finds as a solution to h2
        """
        if len(metadata) != len(self.heuristics):
            raise RuntimeError("Phase independent_set_heuristics was run with invalid length of metadata.")

        for i, h in enumerate(self.heuristics):
            h.run_heuristic(self.G, metadata[i], seed=self.solution) # Note: self.solution is a shallow copy, so solution subset is same throughout.
        self.solution = self.heuristics[len(self.heuristics) - 1].solution
