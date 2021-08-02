from independent_set.heuristics.independent_set_heuristic import IndependentSetHeuristic


class PhaseHeuristic(IndependentSetHeuristic):

    def __init__(self, *argv: [IndependentSetHeuristic]):
        super().__init__(expected_metadata_keys=["metadata"])
        self.heuristics: [IndependentSetHeuristic] = argv

    def _run_heuristic(self, metadata):
        """
            Runs h1, then passes whatever h1 finds as a solution to h2
        """
        if len(metadata) != len(self.heuristics):
            raise RuntimeError("Phase independent_set_heuristics was run with invalid length of metadata.")

        for i, h in enumerate(self.heuristics):
            h.run_heuristic(self.G, metadata[i], self.solution) # Note: self.solution is a shallow copy, so solution subset is same throughout.
        self.solution = self.heuristics[len(self.heuristics) - 1].solution