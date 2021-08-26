from datetime import date
from typing import List

from util.results.result_tensor import ResultTensor


def generate_basic_heuristic_results_file_name() -> str:
    return f"basic-heuristic-results-{date.today()}"


class BasicHeuristicResults:

    def __init__(self, n_values: [int], num_trials: int):
        self.n_values = n_values
        self.num_trials = num_trials
        self.trials = list(range(num_trials))

        self.__chromatic_numbers = ResultTensor()
        self.__chromatic_numbers.add_dimension("n", self.n_values)
        self.__chromatic_numbers.add_dimension("trial", self.trials)
        self.__chromatic_numbers.fix_dimensions()

        self.__heuristic_results = ResultTensor()
        self.__heuristic_results.add_dimension("n", self.n_values)
        self.__heuristic_results.add_dimension("trial", self.trials)
        self.__heuristic_results.fix_dimensions()

    def get_requested_result(self, requested: str) -> List[List[tuple]]:
        r: List[List[tuple]] = []
        pull_from: ResultTensor = {
            'true_chromatics': self.__chromatic_numbers,
            'found_chromatics': self.__heuristic_results,
        }[requested]
        for n in self.n_values:
            add_trial = []
            for trial in self.trials:
                add_trial.append((n, pull_from.get_results(n=n, trial=trial)))
            r.append(add_trial)
        return r

    def add_result(self, n: int, trial: int, chromatic_number: int, result: int):
        self.__chromatic_numbers.add_result(chromatic_number, n=n, trial=trial)
        self.__heuristic_results.add_result(result, n=n, trial=trial)

    def get_true_chr_numbers(self) -> List[List[tuple]]:
        raise AttributeError("Deprecieated, use get requested results")
        true_chr_numbers: List[List[tuple]] = []
        for n in self.n_values:
            add_trial = []
            for trial in self.trials:
                add_trial.append((n, self.__chromatic_numbers.get_results(n=n, trial=trial)))
            true_chr_numbers.append(add_trial)
        return true_chr_numbers

    def get_found_chr_numbers(self) -> List[List[tuple]]:

        raise AttributeError("Deprecieated, use get requested results")
        found_chr_numbers: List[List[tuple]] = []
        for n in self.n_values:
            add_trial = []
            for trial in self.trials:
                add_trial.append((n, self.__heuristic_results.get_results(n=n, trial=trial)))
            found_chr_numbers.append(add_trial)
        return found_chr_numbers
