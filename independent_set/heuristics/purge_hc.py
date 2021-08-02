from util.independent_set_heuristics.heuristic import SeededHeuristic

"""
    Description: IndependentSetHeuristic which takes an initial set in it's solution, then greedily selects
    the highest degree vertex to remove, repeating until the set remaining is an independent
    set.
"""
class GreedySubsetHillClimbing(SeededHeuristic):
    def __init__(self, include_purge: bool = True):
        super().__init__(expected_metadata_keys=["verbose"])
    
    def _run_heuristic(self, verbose):
        while self.solution.num_edges() > 0:
            # While we have edges that we can remove
            rem, rem_deg = self.solution.max_internal_degree(self.solution.subset)
            self.solution.remove_node(rem)
            if verbose:
                print(f"[V] Removed {rem}\t Degree{deg}")
                print(f"[V] # Edges = {self.solution.num_edges}")