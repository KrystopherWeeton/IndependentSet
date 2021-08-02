from datetime import date

from independent_set.result_models.result_tensor import ResultTensor


# TODO: Fix this and move result_tensor to util


def generate_basic_heuristic_results_file_name() -> str:
    return f"basic-heuristic-results-{date.today()}"


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
