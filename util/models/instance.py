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

    def neighbors(self, v: Solution) -> List[Solution]:
        raise NotImplementedError("Create instance subclass")

    @staticmethod
    def generate_random_instance(n: int) -> "Instance":
        raise NotImplementedError("Create instance subclass")
