from datetime import date

# TODO: Fix this and move result_tensor to util
from independent_set.result_models.result_tensor import ResultTensor


def generate_basic_heuristic_results_file_name() -> str:
    return f"basic-heuristic-results-{date.today()}"


class BasicHeuristicResults:

    def __init__(self, n_values: [int], num_trials: int):
        self.n_values = n_values
        self.num_trials = num_trials
        self.trials = range(num_trials)

        self.__chromatic_numbers = ResultTensor()
        self.__chromatic_numbers.add_dimension("n", self.n_values)
        self.__chromatic_numbers.add_dimension("trial", self.trials)
        self.__chromatic_numbers.fix_dimensions()

        self.__heuristic_results = ResultTensor()
        self.__heuristic_results.add_dimension("n", self.n_values)
        self.__heuristic_results.add_dimension("trial", self.trials)
        self.__heuristic_results.fix_dimensions()

    def add_result(self, n: int, trial: int, chromatic_number: int, result: int):
        self.__chromatic_numbers.add_result(chromatic_number, n=n, trial=trial)
        self.__heuristic_results.add_result(result, n=n, trial=trial)

    def get_all_true_chr_numbers(self):

        true_chr_numbers: list = []
        for n in self.n_values:
            for trial in self.trials:
                true_chr_numbers.append((n, self.__chromatic_numbers.get_results(n=n, trial=trial)))

        return true_chr_numbers

    def get_all_found_chr_numbers(self):

        found_chr_numbers: list = []
        for n in self.n_values:
            for trial in self.trials:
                found_chr_numbers.append((n, self.__heuristic_results.get_results(n=n, trial=trial)))

        return found_chr_numbers
