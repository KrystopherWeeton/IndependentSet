from datetime import date
import numpy as np

def generate_size_results_file_name() -> str:
    return f"size-results-{date.today()}"

class SizeResults:

    def __init__(self, n_values: [int], trials: int, planted_ind_set_size: int, min_k: int, max_k: int, step: int):
        self.n_values = n_values
        self.trials = trials
        self.planted_ind_set_size = planted_ind_set_size
        self.min_k = min_k
        self.max_k = max_k
        self.step = step

        self.k_values = list(range(min_k, max_k, step))

        self.results = np.zeros((len(self.n_values, self.k_values, trials)))
        self.total_results = self.n_values * self.k_values * trials
        self.collected_results = 0

    
    def add_results(self, n: int, k: int, t: int, results) -> bool:
        n_index: int = self.n_values.index(n)
        k_index: int = self.k_values.index(k)

        if n_index is None or k_index is None or t < 0 or t >= self.trials:
            raise Exception("Attempt to set invalid results entry for size results")
        
        self.results[n][k][t] = 
