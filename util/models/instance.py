from typing import Callable, List

from util.models.solution import Solution

Metric = Callable[[Solution], float]

class Instance:

    metric: Metric = None

    def __init__(self):
        self.metric = None
        pass

    def set_metric(self, metric: Metric):
        self.metric = metric

    """
    Validates that the solution presented is the correct type for this specific instance
    """
    def validate_solution_type(self, v: Solution) -> bool:
        raise NotImplementedError("Create instance subclass")

    """
    Generates a list of all neighbors for a specified instance
    """
    def neighbors(self, v: Solution) -> List[Solution]:
        raise NotImplementedError("Create instance subclass")
    