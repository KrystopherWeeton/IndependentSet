from datetime import date
import numpy as np
from util.results.result_tensor import ResultTensor

def generate_size_results_file_name() -> str:
    return f"size-results-{date.today()}"

class SizeResults:

    def __init__(self, n_values: [int], k_values: [int], trials: int):
        # Store metadata
        self.trials = trials

        # Store ranges / keys for tracker
        self.n_values = n_values
        self.k_values = k_values
        self.trial_values = list(range(trials))

        # Initialize tracking tensore for the results
        self.result: ResultTensor = ResultTensor()
        self.result.add_dimension("n", self.n_values)
        self.result.add_dimension("k", self.k_values)
        self.result.add_dimension("t", self.trial_values)
        self.result.fix_dimensions()


    def add_result(self, n: int, k: int, t: int, value) -> bool:
        self.result.add_result(value, n=n, k=k, t=t)


    def get_avg_heatmap_values(self):
        if not self.result.all_results_collected():
            raise Warning(f"Attempt to get heatmap values for SizeResults with only {self.result.results_collected} / {self.result.results_total}")
            return None
        
        return self.result.collapse_to_matrix()


    def __iter__(self):
        return iter(self.result.get_index_list())