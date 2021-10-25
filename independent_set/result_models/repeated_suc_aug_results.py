from typing import List

from util.models.result import Result
from util.new_graph.models.graph import Graph


class RepeatedSucAugResults(Result):

    result_identifier: str = "rep-suc-aug"

    def __init__(self, n: int, num_trials: int):
        self.n = n
        self.num_trials = num_trials
       

    def add_result(self, trial: int, step: int, intersection: int, non_intersection: int):
        pass
       