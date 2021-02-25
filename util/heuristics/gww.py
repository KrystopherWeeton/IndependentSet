from util.heuristics.heuristic import Heuristic


class GWW(Heuristic):


    def __init__(self):
        super().__init__(expected_metadata_keys=["num_points"])


    def _run_heuristic(self):
        pass