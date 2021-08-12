from independent_set.heuristics.independent_set_heuristic import \
    IndependentSetHeuristic

"""
    Description: IndependentSetHeuristic which takes an initial set in it's solution, then proceeds
    through hill climbing to minimize the number of edges within the set, while keeping
    the size of the set fixed.
"""
class SwapHillClimbing(IndependentSetHeuristic):
    def __init__(self, verbose: bool = False, debug: bool = False):
        super().__init__(expected_metadata_keys=[], verbose=verbose, debug=debug)
    
    def _run_heuristic(self):
        rem, rem_deg = self.solution.max_internal_degree(self.solution.subset)
        add, add_deg = self.solution.min_internal_degree(self.solution.subset_complement)
        while rem_deg > add_deg:
            # While we are able to reduce density
            self.solution.remove_node(rem_deg)
            self.solution.add_node(add_deg)
            self.verbose_print([
                f"Swapping ({rem}, {add})\t Degrees ({rem_deg}, {add_deg})",
                f"# Edges = {self.solution.num_edges()}"
            ])
            rem, rem_deg = self.solution.max_internal_degree(self.solution.subset)
            add, add_deg = self.solution.min_internal_degree(self.solution.subset_complement)
        