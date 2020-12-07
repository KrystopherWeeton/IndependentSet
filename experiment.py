#!env/bin/python3

import click
import math
import networkx as nx
from util.graph import generate_planted_independent_set_graph
from util.local_optimization import LocalOptimizer, BasicLocalOptimizer
from typing import Tuple, List
from util.plot import PlotArgs, create_dir, Series
import random


@click.group()
def run():
    pass


##########################################
#       Configurations
##########################################

# Used to generate directories for the results
def generate_results_directory(n: int, num_trials: int) -> str:
    return f"test-local-search-n={n}-t={num_trials}"

# This is the size of the planted independent set in terms of n
def planted_ind_set_size(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 5

# This is the maximum size that we want for the initial intersection size
def planted_intersection_sizes(n: int) -> (int, int):
    return (5, math.ceil(math.log(n)) * 10)

# This is the number of 'extra' nodes to include in the initial subset
def planted_subset_sizes(n: int) -> (int, int):
    return (10 * math.ceil(math.sqrt(n)) - 10, 10 * math.ceil(math.sqrt(n)))

# The probability that edges exist
EDGE_PROBABILITY: float = 0.5
# Key provided to every node which is part of the planted independent subset
PLANTED_KEY: str = "beta"
# The step size for k and l
STEP_SIZE: int = 20
# The maximum number of steps an optimizer can run before we stop it
MAX_OPTIMIZER_STEPS: int = 200
# Print debug statements to track what is going on
PRINT_DEBUG: bool = True
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
        if l not in self.results[n]:
            self.results[n][l] = {}
        if k not in self.results[n][l]:
            self.results[n][l][k] = [None] * self.num_trials
        self.results[n][l][k][t] = intersection_size 


    def get_average(self, n: int, k: int, l: int) -> float:
        return sum(self.results[n][l][k]) / self.num_trials

    
    def get_largest_l(self, n: int) -> int:
        return max(self.results[n].keys())


    def get_values(self, n: int, l: int) -> Tuple[List[int], List[int]]:
        k_values: [int] = []
        avg_intersection_size: [float] = []

        for k in self.results[n][l].keys():
            k_values.append(k)
            avg_intersection_size.append(self.get_average(n, k, l))

        return (k_values, avg_intersection_size)
    

    def get_value_for_size(self, n: int) -> Tuple[List[int], List[Tuple[List[int], List[int]]]]:
        l_values: [int] = []
        results: List[Tuple[List[int], List[int]]] = []


        for n in self.results.keys():
            for l in self.results[n].keys():
                l_values.append(l)
                results.append(self.get_values(n, l))
        
        return (l_values, results)


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
        if (PRINT_DEBUG):
            print(f"Running experiments for n={n_value} with planted_size={planted_size}")

        k_init, k_final = planted_intersection_sizes(n_value)       # k is the size of the intersection
        l_init, l_final = planted_subset_sizes(n_value)             # l is the size of the headstart set in total

        for t in range(num_trials):
            # Generate a graph of size n with a planted independent set of a specified size
            (G, B) = generate_planted_independent_set_graph(n_value, EDGE_PROBABILITY, planted_size, "key")

            # Pre-process some data out of G
            erdos_nodes: [int] = set(G.nodes).difference(B)

            if PRINT_DEBUG:
                print(f'l_init={l_init}, l_final={l_final}, k_init={k_init}, k_final={k_final}')
            for l in range(l_init, l_final, STEP_SIZE):
                for k in range(k_init, min(k_final, l), STEP_SIZE):
                    if PRINT_DEBUG:
                        print(f"Running l={l}, k={k}")
                    # TODO: Fix bound issues on runs with less than ~500 nodes
                    if len(B) < k:
                        raise RuntimeError("The planted size is smaller than the requested subset size.")
                    if len(erdos_nodes) < l - k:
                        raise RuntimeError(f"Cannot pull {l - k} vertices from {len(erdos_nodes)} vertices.")
                    # Generate an initial subset of the graph that has a provided intersection size
                    init_set: set = set(random.sample(erdos_nodes, k=l - k) + random.sample(B, k=k))

                    # Run the local optimizer and collect results
                    final_subset: set = local_optimizer.optimize(initial=init_set, G=G, max_steps = MAX_OPTIMIZER_STEPS)
                    intersection_size: int = len(final_subset.intersection(B))
                    results.add_results(n_value, t, k, l, intersection_size)


    #? Results have been collected. Create dir and plot results
    for n_value in n:
        dir_name: str = generate_results_directory(n_value, num_trials)
        dir_name = create_dir(dir_name)
        # For now, just pull the largest l value
        l_value = results.get_largest_l(n_value)
        
        # Access results from the result object and plot
        k_values, int_size = results.get_values(n_value, l_value)
        args: PlotArgs = PlotArgs(
            x_title="Headstart Independent Set Size (k)", 
            y_title="Resulting Independent Set Size",
            directory=dir_name,
            title=f"Local Search Performance with headstart (n={n_value}, l={l_value})",
            file_name=f"local-search-results({n_value}, {l_value})",
            series=[Series(x_values = k_values, y_values=int_size, color="r")])
        args.plot()


if __name__ == "__main__":
    run()

"""
SHORTCUTS
./experiment.py test-local-search -n 500
"""