from util.heuristics.heuristic import Heuristic

class Metropolis(Heuristic):

    def __init__(self):
        super().__init__(expected_metadata_keys=["temperature"])
    

    def _run_heuristic(self):
        pass