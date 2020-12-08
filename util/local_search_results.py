from datetime import date

class Results:
    def __init__(self, num_trials: int, n_values: [int], planted_ind_set_size, k_range, l_range):
        #? Set configuration functions

        self.ranges = {}
        self.results = {}
        self.planted_sizes = {}
        self.n_values = n_values
        self.num_trials = num_trials
        self.total_results = 0
        self.collected_results = 0
        for n in n_values:
            self.ranges[n] = {}
            self.results[n] = {}
            self.planted_sizes[n] = planted_ind_set_size(n)
            k_values = k_range(n)
            l_values = l_range(n)
            self.ranges[n]['k'] = k_values
            self.ranges[n]['l'] = l_values
            for k in k_values:
                for l in l_values:
                    self.results[n][(l, k)] = [None] * num_trials
                    self.total_results += num_trials


    # Generates a name that is good for a file for this object
    def generate_file_name(self, override_name: str = None) -> str:
        return f"results-{date.today()}" if not override_name else override_name


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


    # Returns l_values, k_values, intersection sizes
    def get_results(self, n: int) -> ([int], [int], [[int]]):
        # Pull the l and k values that we want to graph
        l_values: [int] = self.ranges[n]['l']
        k_values: [int]  = self.ranges[n]['k']

        # Pull the heights that we want as a 2d array
        heights: [[int]] = []
        for k in k_values:
            row: [int] = [self.get_average(n, k, l) for l in l_values]
            heights.append(row)
        
        return l_values, k_values, heights


    # Runs tests and asserts that bounds work out, so we get an early failure if there is an issue
    def verify_bounds(self):
        # Assert all keys exist
        assert(all([n in self.results and n in self.ranges for n in self.n_values]))

        for n in self.n_values:
            # Check l and k are alright
            l_values: [int] = self.ranges[n]['l']
            k_values: [int] = self.ranges[n]['k']
            for l in l_values:
                for k in k_values:
                    if l < k:
                        raise RuntimeError(f"l={l} < k={k}")


            # Check that we have enough nodes to pull from
            num_planted: int = self.planted_sizes[n]
            not_planted: int = n - num_planted
            max_not_planted: int = max(l_values) - min(k_values)

            if num_planted < max(k_values):
                raise RuntimeError(f"Max k value of {max(k_values)} for n={n} doesn't work with only {num_planted}.")
            if not_planted < max_not_planted:
                raise RuntimeError(f"Will not be able to pull {max_not_planted} values from {not_planted}.")


    def __str__(self):
        return str(self.results)