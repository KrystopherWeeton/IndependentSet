from datetime import date
import numpy as np
from util.results.result_tensor import ResultTensor

def generate_sa_results_file_name() -> str:
    return f"sa-results-{date.today()}"

class SuccAugResults:

    def __init__(self, N_values: [int], K_values: [int], trials: int):
        # Store metadata
        self.trials = trials

        # Store ranges / keys for tracker
        self.N_values = N_values
        self.K_values = K_values
        self.trial_values = list(range(trials))
        N_range = range(max(N_values))

        # Initialize tracking tensors for the results
        self.size_results: ResultTensor = ResultTensor()
        self.size_results.add_dimension("N", self.N_values)
        self.size_results.add_dimension("K", self.K_values)
        self.size_results.add_dimension("step", self.N_range)
        self.size_results.fix_dimensions()

        self.intersection_results: ResultTensor = ResultTensor()
        self.intersection_results.add_dimension("N", self.N_values)
        self.intersection_results.add_dimension("K", self.K_values)
        self.size_results.add_dimension("step", self.N_range)
        self.intersection_results.fix_dimensions()


    """
        Adds a provided result
    """
    def add_result(self, N: int, K: int, step: int, s: int, k: int) -> bool:
        self.size_results.add_result(s, N=N, K=K, step=step)
        self.intersection_results.add_result(k, N=N, K=K, step=step)
