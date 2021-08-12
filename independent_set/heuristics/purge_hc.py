from independent_set.heuristics.independent_set_heuristic import \
    IndependentSetHeuristic

"""
    Description: IndependentSetHeuristic which takes an initial set in it's solution, then greedily selects
    the highest degree vertex to remove, repeating until the set remaining is an independent
    set.
"""
class GreedySubsetHillClimbing(IndependentSetHeuristic):
    def __init__(self, verbose: bool = False, debug: bool = False):
        super().__init__(expected_metadata_keys=[], verbose=verbose, debug=debug)
    
    def _run_heuristic(self):
        while self.solution.num_edges() > 0:
            # While we have edges that we can remove
            rem, rem_deg = self.solution.max_internal_degree(self.solution.subset)
            self.solution.remove_node(rem)
            self.verbose_print([
                f"Removed {rem}\t Degree{rem_deg}",
                f"# Edges = {self.solution.num_edges}"
            ])
