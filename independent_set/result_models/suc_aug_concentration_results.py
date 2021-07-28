import itertools
from datetime import date

import numpy as np

from independent_set.result_models.result_tensor import ResultTensor
from independent_set.result_models.sa_results import SuccAugResults
from typing import List, Tuple, Callable, Dict
from util.tensor import tensor


def generate_suc_aug_concentration_results_file_name() -> str:
    return f"sa-concentration-results-{date.today()}"

class SucAugConcentrationResults:
    # TODO Deal with the fact that there are no `final_results` set in Succ Aug Results. Can probably just get rid of those honestly

    def __init__(self, n: int, min_epsilon: int, max_epsilon: int, num_trials: int, headstart_size: int, planted_ind_set_size: int):
        self.n = n
        self.min_epsilon = min_epsilon
        self.max_epsilon = max_epsilon
        self.num_trials = num_trials
        self.headstart_size = headstart_size
        self.planted_ind_set_size = planted_ind_set_size
        self.epsilon_values: [int] = list(range(max_epsilon + 1, min_epsilon))
        self.trial_values: [int] = list(range(num_trials))
        self.results: Dict[int, SuccAugResults] = { epsilon: SuccAugResults(self.n, self.planted_size, epsilon, self.num_trials, self.headstart_size) for epsilon in self.epsilon_values}

    def add_result(self, epsilon: int, step: int, trial: int, size: int, intersection: int) -> bool:
        validate(epsilon in self.epsilon_values, f"Cannot add result for {epsilon} which is not in the set epsilon values of {epsilon_values}")
        result: SuccAugResults = self.results[epsilon]
        return result.add_result(step, trial, size, intersection)

    def get_results_for_epsilon(self, epsilon: int) -> SuccAugResults:
        validate(epsilon in self.epsilon_values, f"Cannot add result for {epsilon} which is not in the set epsilon values of {epsilon_values}")
        return self.results[epsilon]