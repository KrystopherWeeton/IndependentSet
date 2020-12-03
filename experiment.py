#!env/bin/python3

import click
import math
import networkx as nx
from util.graph import generate_planted_independent_set_graph
from util.local_optimization import LocalOptimizer, BasicLocalOptimizer
import random


@click.group()
def run():
    pass


##########################################
#       Configurations
##########################################

# This is the size of the planted independent set in terms of n
def planted_ind_set_size(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 10

# This is the maximum size that we want for the initial intersection size
def planted_intersection_sizes(n: int) -> (int, int):
    return (10, math.ceil(math.log(n)) * 10)

# This is the number of 'extra' nodes to include in the initial subset
def planted_non_intersection_sizes(n: int) -> (int, int):
    return (10, 2 * math.ceil(math.sqrt(n)))

# The probability that edges exist
EDGE_PROBABILITY: float = 0.5
# Key provided to every node which is part of the planted independent subset
PLANTED_KEY: str = "beta"
# The step size for k and l
STEP_SIZE: int = 10
# The maximum number of steps an optimizer can run before we stop it
MAX_OPTIMIZER_STEPS: int = 999
# The local optimizer used to solve the instance provided
local_optimizer: LocalOptimizer = BasicLocalOptimizer()

##########################################
#       Experiments
##########################################

class Results:
    def __init__(self, num_trials: int):
        self.results = {}
        self.num_trials = num_trials
        pass


    def add_results(self, n: int, t: int, k: int, l: int, intersection_size: int):
        # Initialize what needs to be initialized
        if n not in self.results:
            self.results[n] = {}
        if k not in self.results[n]:
            self.results[n][k] = {}
        if l not in self.results[n][k]:
            self.results[n][k][l] = [None] * self.num_trials
        self.results[n][k][l][t] = intersection_size 


    def get_average(self, n: int, k: int, l: int) -> float:
        return sum(self.results[n][k][l]) / self.num_trials
    

    def get_list(self, n: int, k: int):
        l_values: [int] = []
        average: [float] = []

        data: dict = self.results[n][k]
        for l in data.keys():
            l_values.append(l)
            average.append(self.get_average(n, k, l))
        return (l_values, average)

    def __str__(self):
        return str(self.results)


@run.command()
@click.option("-n", required=True, multiple=True, type=int)
@click.option("--num-trials", required=False, multiple=False, type=int, default=1)
def test_local_search(n: [int], num_trials):
    # TODO: Need to add printing statements which show progress of the algorithm
    if len(n) == 0:      # Initial argument checking
        click.secho("At least one value for n must be provided", fg="red")
    if any([x <= 0 for x in n]):
        click.secho("All values of n must be positive.", fg="red")

    #? Initialization
    random.seed(0)      # TODO: Swap out for randomly seeded randomness when testing is complete
    results: Results = Results(num_trials)


    #? Loop over the different values of n which should be tested
    for n_value in n:
        # Generate metadata about the trial
        planted_size: int = planted_ind_set_size(n_value)
        planted_size = planted_size if planted_size < n_value else n_value

        k_init, k_final = planted_intersection_sizes(n_value)
        l_init, l_final = planted_non_intersection_sizes(n_value)     # l here is the num. of vertices not including the k in the intersection

        for t in range(num_trials):
            # Generate a graph of size n with a planted independent set of a specified size
            (G, B) = generate_planted_independent_set_graph(n_value, EDGE_PROBABILITY, planted_size, "key")

            # Pre-process some data out of G
            erdos_nodes: [int] = set(G.nodes).difference(B)

            for k in range(k_init, k_final, STEP_SIZE):
                for l in range(l_init, l_final, STEP_SIZE):
                    if len(B) < l:
                        raise RuntimeError("The planted size is smaller than the requested subset size.")
                    if len(erdos_nodes) < l:
                        raise RuntimeError("There are not enough non-planted vertices to pull from.")
                    # Generate an initial subset of the graph that has a provided intersection size
                    init_set: set = set(random.sample(erdos_nodes, k=l) + random.sample(B, k=k))

                    # Run the local optimizer and collect results
                    final_subset: set = local_optimizer.optimize(initial=init_set, G=G, max_steps = MAX_OPTIMIZER_STEPS)
                    intersection_size: int = len(final_subset.intersection(B))
                    results.add_results(n_value, t, k, l, intersection_size)

    print("RESULTS:", results.get_list(200, 40))


if __name__ == "__main__":
    run()
