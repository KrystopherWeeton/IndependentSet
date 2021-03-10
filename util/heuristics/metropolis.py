import random
from util.heuristics.heuristic import Heuristic
import util.formulas as formulas
import math

class Metropolis(Heuristic):

    def __init__(self):
        super().__init__(expected_metadata_keys=["temperature", "max_steps"])


    """
        Calculates the threshold when presented with an option that increases density
    """
    def __calc_threshold(self, density: float, temperature: float) -> float:
        threshold = math.e**(-density / temperature)
        if threshold > 1:
            raise Exception(f"Metropolis got a threshold {threshold} > 1.")
        return threshold


    def __select_initial_subset(self):
        # Right now just select a random point
        x = random.choice(list(self.G.nodes))
        return set([x])


    def _run_heuristic(self):
        # Set initial solution to initial subset selected
        self.solution.set_subset(self.__select_initial_subset())

        # Load metadata into variables
        max_steps: int = self.metadata["max_steps"]
        temperature: float = self.metadata["temperature"]

        # Perform actual metropolis process
        for i in range(max_steps):
            k: int = self.solution.size()

            #? Generate a candidate and calculate new density
            node: int = random.choice(list(self.G.nodes))
            removing: bool = node in self.solution
            internal_degree: int = self.solution.internal_degree(node)
            if removing:
                new_density: float = formulas.density_after_rem(self.solution.density(), k, internal_degree)
            else:
                new_density: float = formulas.density_after_add(self.solution.density(), k, internal_degree)

            #? Calculate acceptance threshold, determine action
            threshold: float = self.__calc_threshold(new_density, temperature)
            if random.random() <= threshold:
                if removing:
                    self.solution.remove_node(node)
                else:
                    self.solution.add_node(node)

        # Ran out of steps. Give warning then bail
        print(
            f"Warning: Metropolis ran {max_steps} without terminating."
        )
        return


TESTING_METADATA: dict = {
    "temperature": 0.5,
    "max_steps": 999
}