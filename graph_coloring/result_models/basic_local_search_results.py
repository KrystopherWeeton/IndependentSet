from datetime import date
from typing import List

from independent_set.result_models.result_tensor import ResultTensor


# TODO: Fix this and move result_tensor to util


def generate_basic_local_search_results_file_name() -> str:
    return f"basic-local-search-results-{date.today()}"


class BasicLocalSearchResults:

    def __init__(self, n_values: [int], num_trials: int):
        self.n_values = n_values
        self.num_trials = num_trials
        self.trials = range(num_trials)

        self.__num_conflicting_edges = ResultTensor()
        self.__num_conflicting_edges.add_dimension("n", self.n_values)
        self.__num_conflicting_edges.add_dimension("trial", self.trials)
        self.__num_conflicting_edges.fix_dimensions()

        self.__iterations = ResultTensor()
        self.__iterations.add_dimension("n", self.n_values)
        self.__iterations.add_dimension("trial", self.trials)
        self.__iterations.fix_dimensions()

    def add_result(self, n: int, trial: int, iterations_taken: int, num_conflicting_edges: int):
        self.__iterations.add_result(iterations_taken, n=n, trial=trial)

        self.__num_conflicting_edges.add_result(num_conflicting_edges, n=n, trial=trial)

    def get_num_conflicting_edges(self) -> List[List[tuple]]:

        true_chr_numbers: List[List[tuple]] = []
        for n in self.n_values:
            add_trial = []
            for trial in self.trials:
                add_trial.append((n, self.__num_conflicting_edges.get_results(n=n, trial=trial)))
            true_chr_numbers.append(add_trial)
        return true_chr_numbers

    def get_iterations_taken(self) -> List[List[tuple]]:

        found_chr_numbers: List[List[tuple]] = []
        for n in self.n_values:
            add_trial = []
            for trial in self.trials:
                add_trial.append((n, self.__iterations.get_results(n=n, trial=trial)))
            found_chr_numbers.append(add_trial)
        return found_chr_numbers
