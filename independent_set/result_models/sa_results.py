import itertools
from datetime import date
from typing import Callable, List, Tuple

import numpy as np

from util.models.result import Result
from util.results.result_tensor import ResultTensor
from util.tensor import tensor


class SuccAugResults(Result):

    result_identifier: str = "sa-results"

    def __init__(self, n: int, planted_size: int, epsilon: int, trials: int, headstart_size: int):
        # Store metadata
        self.trials = trials
        self.headstart_size: int = headstart_size
        self.epsilon: int = epsilon

        # Store ranges / keys for tracker
        self.trial_values = list(range(trials))
        self.step_values = list(range(n - headstart_size))
        self.n = n
        self.planted_size = planted_size

        # Initialize tracking tensors for the results
        self.size_results: ResultTensor = ResultTensor()
        self.size_results.add_dimension("step", self.step_values)
        self.size_results.add_dimension("trial", self.trial_values)
        self.size_results.fix_dimensions()

        self.intersection_results: ResultTensor = ResultTensor()
        self.intersection_results.add_dimension("step", self.step_values)
        self.intersection_results.add_dimension("trial", self.trial_values)
        self.intersection_results.fix_dimensions()


    """
        Adds a provided result
    """
    def add_result(self, step: int, trial: int, size: int, intersection: int) -> bool:
        self.size_results.add_result(size, step=step, trial=trial)
        self.intersection_results.add_result(intersection, step=step, trial=trial)
    

    def add_final_results(self, size: int, intersection: int):
        self.final_size: int = size
        self.final_intersection: int = intersection


    def for_each_trial_results(self, f: Callable):
        """
            Runs the provided function `f` on each trial value, where `f(trial_num, size_results, intersection_results) is the function structure
        """
        for t in self.trial_values:
            sizes: List[int] = list(self.size_results.get_sub_tensor("trial", t))
            intersections: List[int] = list(self.intersection_results.get_sub_tensor("trial", t))
            f(t, sizes, intersections)


    def __iter__(self):
        return iter(self.trial_values)
