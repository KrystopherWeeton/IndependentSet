from itertools import product
from typing import Callable, Dict, List, Tuple

from numpy.core.fromnumeric import prod

from util.models.instance import Instance, Metric
from util.models.solution import Solution
from util.new_graph.models.graph import Graph, generate_planted_ind_set_graph


class IndSetSolution(Solution, set):

    def __init__(self, s=()):
        super(IndSetSolution,self).__init__(s)


"""
    Testing solution space tracker, where swaps are allowed.
"""
class IndSetInstance(Instance):

    metric: Metric = None
    g: Graph = None

    def __init__(self, g: Graph):
        self.set_metric(lambda x: 1)
        self.g = g

    def validate_solution_type(self, v: Solution) -> bool:
        return v is set

    """
    Generates a list of all neighbors for a specified instance
    """
    def neighbors(self, v: set) -> List[Solution]:
        not_included: List[int] = self.g.vertex_set().symmetric_difference(v)
        swaps: List[Tuple[int, int]] = product(v, not_included)
        l: List[Solution] = []
        for s in swaps:
            other = v.copy()
            other.remove(s[0])
            other.add(s[1])
            l.append(other)
        return l

    @staticmethod
    def generate_random_instance(n: int, planted_size: int) -> "Instance":
        return Instance(generate_planted_ind_set_graph(n, 0.5, planted_size))

