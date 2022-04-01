import random
from copy import copy
from typing import Callable, List, Set, Tuple

from networkx.algorithms.similarity import debug_print
from numpy import sort
from sympy import re

from error_correcting_codes.models.algorithms.algorithm import Algorithm
from independent_set.heuristics.independent_set_heuristic import \
    IndependentSetHeuristic
from util.graph import count_edge_boundary
from util.models.graph_subset_tracker import GraphSubsetTracker, get_density
from util.new_graph.models.graph import Graph
from util.new_graph.util import uniformly_sample_subset


class SparseBacktracking(Algorithm):


    def __init__(self, verbose=False, debug=False, step_hook = None):
        super().__init__(Set, verbose, debug)
        self._step_hook = step_hook


    def _branch(self, G: Graph, remaining: Set[int], subset: Set[int]):
        self.calls += 1
        # Base Case were done
        if len(remaining) == 0:
            # Score and return subset
            return subset

        # Non Base Case, check for degree into remaining vertices
        v: int = remaining.pop()
        set_v: Set[int] = set([v])
        degree: int = G.edge_boundary(v, remaining)
        next_rem: Set[int] = remaining.difference(set_v)

        #print(f"Branching {v}, degree {degree}")
        if degree == 0:
            # Always include if degree is 0
            # Don't worry about updating remaining
            return self._branch(G, next_rem, subset.union(set_v))
        elif degree == 1:
            """
                If degree is one, we always want to add still. We want to add either v or u (other side of edge). If u also has
                degree 1, then it doesn't matter which. If u has degree > 1, then adding v removes u, but adding u removes v along
                with the other vertices from contention so we may as well add u.
            """
            return self._branch(G, next_rem.difference(G.neighbors(v)), subset.union(set_v))
        else:
            # Case 1: We want to include v
            s1: Set[int] = self._branch(G, next_rem.difference(G.neighbors(v)), subset.union(set_v))
            # Case 2: We dont want to include v
            s2: Set[int] = self._branch(G, next_rem, subset)
            return s1 if len(s1) > len(s2) else s2

    def _clear(self):
        self.calls: int = 0
        pass


    def _pre_process(self, remaining_vertices: Set[int], G: Graph) -> Set[int]:
        sol: Set[int] = set([])
        temp: Set[int] = copy(remaining_vertices)
        while len(temp) > 0:
            v = temp.pop()
            con_vertices: Set[int] = G.connected_vertices(v, remaining_vertices)
            d: int = len(con_vertices)
            if d == 0:
                sol.add(v)
                remaining_vertices.remove(v)
            elif d == 1:
                sol.add(v)
                u: int = con_vertices.pop()
                remaining_vertices.remove(v)
                remaining_vertices.remove(u)
                print(v, remaining_vertices, temp)
                if u in temp:
                    temp.remove(u)
        return sol


    def _run(self, 
        G: Graph,
    ):
        """
            (1) Take every vertex that has 0 degree
            (2) Sort remaining vertices by increasing degree, and split off of lower degree
            (3) For 1 degree vertices I think we always want to add? We either add this or the other side,
            if we add the other side it has at least degree one, so it removes at least 1 from contention, so no reason to include.
            Actually just fold this into pre-processing.
        """
        sol: Set[int] = set([])
        step: Set[int] = None
        remaining_vertices: Set[int] = G.vertex_set()
        made_progress: int = True

        while made_progress:
            step = self._pre_process(remaining_vertices, G)
            sol = sol.union(step)
            made_progress = len(step) > 0
            print(f"Remaining Vertices: {remaining_vertices}")
            print(f"Solution: {sol}")
            print(F"Step: {step}")

        self._solution: Set[int] = self._branch(G, remaining_vertices, sol)
