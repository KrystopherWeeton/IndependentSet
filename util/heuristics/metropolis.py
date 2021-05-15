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


    def __select_initial_subset(self) -> set:
        '''
        # Right now just select a random point
        x = random.choice(list(self.G.nodes))
        '''
        print(random.sample(list(self.G.nodes), math.ceil(math.sqrt(self.G.number_of_nodes()))))
        subset1 = set(random.sample(list(self.G.nodes), math.ceil(math.sqrt(self.G.number_of_nodes()))))
        return subset1


    def _run_heuristic(self):
        # Set initial solution to initial subset selected
        self.solution.set_subset(self.__select_initial_subset())

        # Load metadata into variables
        max_steps: int = self.metadata["max_steps"]
        temperature: float = self.metadata["temperature"]

        # Perform actual metropolis process
        for i in range(max_steps):
            k: int = self.solution.size()
            ''' OLD CODE
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
            '''
            # Eric's code:
            #? Generate a candidate and calculate new density
            node_remove: int = random.choice(list(self.solution.subset))
            node_add: int = random.choice(list(self.solution.vertices_not_in_subset))
            #new_density: float = (self.solution.__edges_in_subset - self.solution.internal_degree(node_remove) + self.solution.internal_degree(node_add)) / self.solution.__density_size_constant
            new_density: float = formulas.updated_density_after_swap(self.solution.edges_in_subset, self.solution.internal_degree(node_remove), self.solution.internal_degree(node_add), self.solution.density_size_constant)
            # Edge case: if node_remove and node_add have an edge between them, in the swap they will still have an edge.  Similarly, if no edge, still no edge, so we don't need to worry about that
            # perform swap
            #? Calculate acceptance threshold, determine action
            threshold: float = self.__calc_threshold(new_density, temperature)
            if random.random() <= threshold:
                self.solution.add_node(node_add)
                self.solution.remove_node(node_remove)
            # End Eric's code


        # Ran out of steps. Give warning then bail
        print(
            f"Warning: Metropolis ran {max_steps} without terminating."
        )
        return


TESTING_METADATA: dict = {
    "temperature": 0.5,
    "max_steps": 999
}