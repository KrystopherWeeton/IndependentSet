from typing import List, Set

from independent_set.heuristics.independent_set_heuristic import \
    IndependentSetHeuristic
from util.models.graph_subset_tracker import GraphSubsetTracker


class CombineHeuristicSolutions(IndependentSetHeuristic):

    def __init__(self, *argv: List[IndependentSetHeuristic], verbose: bool = False, debug: bool = False):
        super().__init__(expected_metadata_keys=["metadata"], verbose=verbose, debug=debug)
        self.heuristics: List[IndependentSetHeuristic] = argv

    def _run_heuristic(self, metadatas, combine_strategy):
        """
            Runs h1, then passes whatever h1 finds as a solution to h2
        """
        if len(metadatas) != len(self.heuristics):
            raise RuntimeError("Phase independent_set_heuristics was run with invalid length of metadata.")

        # Run each heuristic to get the things
        for i, h in enumerate(self.heuristics):
            h.run_heuristic(self.G, metadatas[
                i])  # Note: self.solution is a shallow copy, so solution subset is same throughout.

        self.solution: GraphSubsetTracker = {
            "intersection_of_neighborhoods": self.__intersection_of_neighborhoods
        }['combine_strategy']()

    def __intersection_of_neighborhoods(self) -> GraphSubsetTracker:
        # Create the neighborhoods for each of them
        neighborhoods: List[Set[int]] = []

        for h in self.heuristics:
            nbhood_to_add: Set[int] = set()

            for node in h.solution.subset():
                nbhood_to_add.union(self.G[node])
            neighborhoods.append(nbhood_to_add)

        return GraphSubsetTracker(self.G, neighborhoods[0].intersection(*neighborhoods))
