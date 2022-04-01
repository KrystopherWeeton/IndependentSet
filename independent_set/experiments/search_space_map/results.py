from argparse import ArgumentError
from collections import namedtuple
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from util.models.result import Result
from util.results.result_series import ResultSeries


class SearchSpaceMapResults(Result):

    result_identifier: str = "correction-series-results"

    def __init__(self, n: int, k: int, j: int, p_values: List[float], num_trials: int):
        pass

    
    def add_result(self, parity: int, hamming_dist: int, p: float, trial: int):
        pass
