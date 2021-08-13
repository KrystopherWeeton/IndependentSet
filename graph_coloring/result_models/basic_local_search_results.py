from datetime import date
from typing import List

from util.results.result_tensor import ResultTensor

ITERATIONS = 'iterations'
NUM_CONFLICTING_EDGES = 'num_conflicting_edges'
CHROMATIC_NUMBER = 'chromatic_number'




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

        self.__chromatic_numbers = ResultTensor()
        self.__chromatic_numbers.add_dimension("n", self.n_values)
        self.__chromatic_numbers.add_dimension("trial", self.trials)
        self.__chromatic_numbers.fix_dimensions()

    def add_result(self, n: int, trial: int, iterations_taken: int, num_conflicting_edges: int, chromatic_number: int):
        self.__iterations.add_result(iterations_taken, n=n, trial=trial)

        self.__num_conflicting_edges.add_result(num_conflicting_edges, n=n, trial=trial)

        self.__chromatic_numbers.add_result(chromatic_number, n=n, trial=trial)

    def get_results(self, requested: str) -> List[List[tuple]]:
        res: List[List[tuple]] = []
        list_to_query: ResultTensor = (
            self.__num_conflicting_edges if requested == NUM_CONFLICTING_EDGES else (
                self.__chromatic_numbers if requested == CHROMATIC_NUMBER else (
                    self.__iterations if requested == ITERATIONS else None
                )
            )
        )
        if list_to_query == None:
            raise AttributeError("You're requesting data that doesn't exist!")

        for n in self.n_values:
            add_trial = []
            for trial in self.trials:
                add_trial.append((n, list_to_query.get_results(n=n, trial=trial)))
            res.append(add_trial)
        return res

    # TODO: Depreciated, remove

    #
    # def get_num_conflicting_edges(self) -> List[List[tuple]]:
    #
    #     num_conf_edges: List[List[tuple]] = []
    #     for n in self.n_values:
    #         add_trial = []
    #         for trial in self.trials:
    #             add_trial.append((n, self.__num_conflicting_edges.get_results(n=n, trial=trial)))
    #         num_conf_edges.append(add_trial)
    #     return num_conf_edges
    #
    # def get_true_chr_numbers(self) -> List[List[tuple]]:
    #
    #     true_chr_numbers: List[List[tuple]] = []
    #     for n in self.n_values:
    #         add_trial = []
    #         for trial in self.trials:
    #             add_trial.append((n, self.__chromatic_numbers.get_results(n=n, trial=trial)))
    #         true_chr_numbers.append(add_trial)
    #     return true_chr_numbers
    #
    # def get_iterations_taken(self) -> List[List[tuple]]:
    #
    #     iterations: List[List[tuple]] = []
    #     for n in self.n_values:
    #         add_trial = []
    #         for trial in self.trials:
    #             add_trial.append((n, self.__iterations.get_results(n=n, trial=trial)))
    #         iterations.append(add_trial)
    #     return iterations
