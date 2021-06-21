from datetime import date
import numpy as np
from util.results.result_tensor import ResultTensor
import itertools

def generate_sa_results_file_name() -> str:
    return f"sa-results-{date.today()}"

class SuccAugResults:

    def __init__(self, n: int, planted_size: int, trials: int):
        # Store metadata
        self.trials = trials

        # Store ranges / keys for tracker
        self.trial_values = list(range(trials))
        self.n = n
        self.planted_size = planted_size

        # Initialize tracking tensors for the results
        self.size_results: ResultTensor = ResultTensor()
        self.size_results.add_dimension("step", list(range(n)))
        self.size_results.add_dimension("trial", self.trial_values)
        self.size_results.fix_dimensions()

        self.intersection_results: ResultTensor = ResultTensor()
        self.intersection_results.add_dimension("step", list(range(n)))
        self.intersection_results.add_dimension("trial", self.trial_values)
        self.intersection_results.fix_dimensions()


    """
        Adds a provided result
    """
    def add_result(self, step: int, trial: int, size: int, intersection: int) -> bool:
        self.size_results.add_result(size, step=step, trial=trial)
        self.intersection_results.add_result(intersection, step=step, trial=trial)


    def __iter__(self):
        return iter(self.trial_values)