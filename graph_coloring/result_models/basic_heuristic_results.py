from datetime import date
from typing import List

from graph_coloring.experiments.common import CENTER_SET_SIZE
from util.results.result_tensor import ResultTensor


def generate_basic_heuristic_results_file_name() -> str:
    return f"basic-heuristic-results-{date.today()}"


class BasicHeuristicResults:

    def __init__(self, n_values: [int], num_trials: int, experiments: [str] = ['true_vs_found']):
        self.n_values = n_values
        self.num_trials = num_trials
        self.trials = range(num_trials)

        self.experiments = experiments
        self.__chromatic_numbers = None
        self.__heuristic_results = None
        self.__center_set_sizes = None
        self.__num_uncolored = None
        if 'true_vs_found' in self.experiments:
            self.__chromatic_numbers = ResultTensor()
            self.__chromatic_numbers.add_dimension("n", self.n_values)
            self.__chromatic_numbers.add_dimension("trial", self.trials)
            self.__chromatic_numbers.fix_dimensions()

            self.__heuristic_results = ResultTensor()
            self.__heuristic_results.add_dimension("n", self.n_values)
            self.__heuristic_results.add_dimension("trial", self.trials)
            self.__heuristic_results.fix_dimensions()

        if CENTER_SET_SIZE in self.experiments:
            self.__center_set_sizes = ResultTensor()
            self.__center_set_sizes.add_dimension('n', self.n_values)
            self.__center_set_sizes.add_dimension('trial', self.trials)
            self.__center_set_sizes.fix_dimensions()

            self.__num_uncolored = ResultTensor()
            self.__num_uncolored.add_dimension('n', self.n_values)
            self.__num_uncolored.add_dimension('trial', self.trials)
            self.__num_uncolored.fix_dimensions()

    # TODO: switch to kwargs
    def add_result(
            self, n: int,
            trial: int,
            chromatic_number: int = None,
            result: int = None,
            cc_siz: int = None,
            num_un: int = None
    ):
        if 'true_vs_found' in self.experiments:
            self.__chromatic_numbers.add_result(chromatic_number, n=n, trial=trial)
            self.__heuristic_results.add_result(result, n=n, trial=trial)
        if CENTER_SET_SIZE in self.experiments:
            self.__center_set_sizes.add_result(cc_siz, n=n, trial=trial)
            self.__num_uncolored.add_result(num_un, n=n, trial=trial)

    def get_requested_result(self, requested: str) -> List[List[tuple]]:
        r: List[List[tuple]] = []
        pull_from: ResultTensor = {
            'true_chromatics': self.__chromatic_numbers,
            'found_chromatics': self.__heuristic_results,
            'center_set_sizes': self.__center_set_sizes,
            'num_uncolored': self.__num_uncolored
        }[requested]
        for n in self.n_values:
            add_trial = []
            for trial in self.trials:
                add_trial.append((n, pull_from.get_results(n=n, trial=trial)))
            r.append(add_trial)
        return r

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
