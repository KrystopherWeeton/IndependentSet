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
    return (5, math.ceil(math.log(n)) * 5)

# This is the number of 'extra' nodes to include in the initial subset
def planted_subset_sizes(n: int) -> (int, int):
    return (10 * math.ceil(math.sqrt(n)) - 20, 10 * math.ceil(math.sqrt(n)))

# The probability that edges exist
EDGE_PROBABILITY: float = 0.5
# Key provided to every node which is part of the planted independent subset
PLANTED_KEY: str = "beta"
# The step size for k and l
STEP_SIZE: int = 20
# The maximum number of steps an optimizer can run before we stop it
MAX_OPTIMIZER_STEPS: int = 200
# Print debug statements to track what is going on
PRINT_DEBUG: bool = False
# The percent to accomplish between each print statement
PERCENT_INCREMENT: float = 0.05
# The local optimizer used to solve the instance provided
local_optimizer: LocalOptimizer = BasicLocalOptimizer()

##########################################
#       Experiments
##########################################

class Results:
    def __init__(self, num_trials: int, n_values: [int]):
        self.ranges = {}
        self.results = {}
        self.n_values = n_values
        self.num_trials = num_trials
        self.total_results = 0
        self.collected_results = 0
        for n in n_values:
            self.ranges[n] = {}
            self.results[n] = {}
            k_init, k_final = planted_intersection_sizes(n)       # k is the size of the intersection
            l_init, l_final = planted_subset_sizes(n)             # l is the size of the headstart set in total
            k_values = list(range(k_init, k_final, STEP_SIZE))
            l_values = list(range(l_init, l_final, STEP_SIZE))
            self.ranges[n]['k'] = k_values
            self.ranges[n]['l'] = l_values
            for k in k_values:
                for l in l_values:
                    self.results[n][(l, k)] = [None] * num_trials
                    self.total_results += num_trials


    # Gets the ranges to be used for a specific experiment
    def get_ranges(self, n: int) -> ([int], [int]):
        if n not in self.ranges:
            raise RuntimeError(f"Attempt to access range for {n}, which has not been initialized in ranges.")
        return (self.ranges[n]['k'], self.ranges[n]['l'])


    # Adds results for a trial
    def add_results(self, n: int, t: int, k: int, l: int, intersection_size: int):
        self.results[n][(l, k)][t] = intersection_size
        self.collected_results += 1

    # Gets the average for a specific experiment across trials
    def get_average(self, n: int, k: int, l: int) -> float:
        return sum(self.results[n][(l, k)]) / self.num_trials


    # Gets the % of total results which have been collected
    def get_percent_complete(self) -> float:
        return self.collected_results / self.total_results


    def get_largest_l(self, n: int) -> int:
        return max(self.results[n].keys(), key=lambda x : x[0])[0]


    def get_values(self, n: int, l: int) -> Tuple[List[int], List[int]]:
        k_values: [int] = []
        avg_intersection_size: [float] = []

        for (l_value, k) in self.results[n].keys():
            if l != l_value:
                continue

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

    # Runs tests and asserts that bounds work out, so we get an early failure if there is an issue
    def verify_bounds(self):
        # Assert all keys exist
        assert(all([n in self.results and n in self.ranges for n in self.n_values]))

        for n in self.n_values:
            l_values: [int] = self.ranges[n]['l']
            k_values: [int] = self.ranges[n]['k']
            for i in range(len(l_values)):
                # Assert that we have a larger subset than the intersection size
                assert(l_values[i] >= k_values[i])


    def __str__(self):
        return str(self.results)


@run.command()
@click.option("-n", required=True, multiple=True, type=int)
@click.option("--num-trials", required=False, multiple=False, type=int, default=1)
def test_local_search(n: [int], num_trials):
    #? Verify command line arguments make sense
    if len(n) == 0:      # Initial argument checking
        click.secho("At least one value for n must be provided", fg="red")
    if any([x <= 0 for x in n]):
        click.secho("All values of n must be positive.", fg="red")

    #? Initialization
    random.seed(0)      # TODO: Swap out for randomly seeded randomness when testing is complete
    results: Results = Results(num_trials, n)
    percent_done: float = 0
    results.verify_bounds()                         # Run initial tests just to verify bounds work out
    if PRINT_DEBUG:
        print(f"Verification of k and l values has passed. Starting...")


    #? Loop over the different values of n which should be tested
    for n_value in n:
        # Generate metadata about the trial
        planted_size: int = planted_ind_set_size(n_value)
        planted_size = planted_size if planted_size < n_value else n_value
        if (PRINT_DEBUG):
            print(f"Running experiments for n={n_value} with planted_size={planted_size}")
        
        k_values, l_values = results.get_ranges(n_value)

        for t in range(num_trials):
            # Generate a graph of size n with a planted independent set of a specified size
            (G, B) = generate_planted_independent_set_graph(n_value, EDGE_PROBABILITY, planted_size, "key")

            # Pre-process some data out of G
            erdos_nodes: [int] = set(G.nodes).difference(B)

            for l in l_values:
                for k in k_values:
                    # TODO: Fix bound issues on runs with less than ~500 nodes
                    if PRINT_DEBUG:
                        print(f"Running l={l}, k={k}")
                    if len(B) < k:
                        raise RuntimeError("The planted size is smaller than the requested subset size.")
                    if len(erdos_nodes) < l - k:
                        raise RuntimeError(f"Cannot pull {l - k} vertices from {len(erdos_nodes)} vertices.")
                    if l < k:
                        raise RuntimeError(f"Cannot run experiment with l={l} < k={k}")

                    # Generate an initial subset of the graph that has a provided intersection size
                    init_set: set = set(random.sample(erdos_nodes, k=l-k) + random.sample(B, k=k))

                    # Run the local optimizer and collect results
                    final_subset: set = local_optimizer.optimize(initial=init_set, G=G, max_steps = MAX_OPTIMIZER_STEPS)
                    intersection_size: int = len(final_subset.intersection(B))
                    results.add_results(n_value, t, k, l, intersection_size)
                    if results.get_percent_complete() > percent_done + PERCENT_INCREMENT:
                        percent_done = results.get_percent_complete()
                        print(f"{int(percent_done * 100)}% Complete")
    
    if PRINT_DEBUG:
        print(f"Ranges: {results.ranges}")


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
./experiment.py test-local-search -n 200
"""