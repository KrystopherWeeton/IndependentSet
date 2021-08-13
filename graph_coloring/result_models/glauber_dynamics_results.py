from datetime import date

from util.results.result_tensor import ResultTensor


def generate_basic_heuristic_results_file_name() -> str:
    return f"basic-heuristic-results-{date.today()}"


class GlauberDynamicsResults:

    def __init__(self, n_values: [int], num_trials: int):
        self.n_values = n_values
        self.num_trials = num_trials
        self.trials = range(num_trials)

        self.__iterations = ResultTensor()
        self.__iterations.add_dimension("n", self.n_values)
        self.__iterations.add_dimension("trial", self.trials)
        self.__iterations.fix_dimensions()

    def add_result(self, n: int, trial: int, iterations_taken: int):
        self.__iterations.add_result(iterations_taken, n=n, trial=trial)
