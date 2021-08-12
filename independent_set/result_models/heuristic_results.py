import inspect
from datetime import date
from typing import List

import util.formulas as formulas
from util.models.result import Result
from util.models.stat_info import StatInfo


class HeuristicResults(Result):

    result_identifier: str = "heuristic-results"

    def __init__(self, n_values: List[int], num_trials: int, planted_ind_set_size, metadata: dict):
        #? Set configuration values
        self.n_values = n_values
        self.num_trials = num_trials
        # The size of the planted independent set sizes
        self.planted_sizes = {}
        # The results themselves, indexed by n values
        self.results = {}

        self.heuristic_metadata = {}
        for k in metadata.keys():
            if callable(metadata[k]):
                self.heuristic_metadata[k] = inspect.getsourcelines(metadata[k])[0][0]
            else:
                self.heuristic_metadata[k] = metadata[k]
        
        #? Set configuration values which require calculation
        # The number of results which need to be collected to complete the results
        self.total_results = len(self.n_values) * num_trials
        self.collected_results = 0
        # The actual result objects
        for n in self.n_values:
            self.planted_sizes[n] = planted_ind_set_size(n)
            self.results[n] = {}
            self.results[n]["intersection_size"] = [None] * self.num_trials
            self.results[n]["density"] = [None] * self.num_trials
            self.results[n]["subset_size"] = [None] * self.num_trials


    def add_result(self, n: int, t: int, intersection_size: int, density: float, subset_size: int):
        self.results[n]['intersection_size'][t] = intersection_size
        self.results[n]['density'][t] = density
        self.results[n]['subset_size'][t] = subset_size
        self.collected_results += 1

    #? Stuff for accessing / interpreting results

    def get_results(self, n: int, key: str) -> List[float]:
        return self.results[n][key]

    
    def get_n_values(self) -> List[int]:
        return self.n_values

    
    def get_density_info(self, n: int) -> StatInfo:
        info: StatInfo = StatInfo(self.get_results(n, "density"))
        return info


    def get_subset_size_info(self, n: int) -> StatInfo:
        info: StatInfo = StatInfo(self.get_results(n, "subset_size"))
        return info


    def get_intersection_info(self, n: int) -> StatInfo:
        info: StatInfo = StatInfo(self.get_results(n, "intersection_size"))
        return info


    def get_all_density_info(self) -> List[StatInfo]:
        return [ self.get_density_info(n) for n in self.n_values]

    
    def get_all_subset_size_info(self) -> List[StatInfo]:
        return [ self.get_subset_size_info(n) for n in self.n_values]


    def get_all_intersection_size_info(self) -> List[StatInfo]:
        return [ self.get_intersection_info(n) for n in self.n_values]

    
    def get_subset_size_data(self) -> List[List[float]]:
        return [
            self.get_results(n, "subset_size") for n in self.n_values
        ]


    def get_intersection_data(self) -> List[List[float]]:
        return [
            self.get_results(n, "intersection_size") for n in self.n_values
        ]
