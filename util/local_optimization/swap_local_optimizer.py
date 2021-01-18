from util.local_optimization.local_optimization import *
import networkx as nx
import numpy as np

class SwapLocalOptimizer(LocalOptimizer):
    def __init__(self):
        pass


    def optimizer(self, initial: set, G: nx.graph, max_steps: int) -> set:
        self._reset(G, initial)
        for i in range(max_steps):
            swap: SwapUpdate = self._get_best_swap()
            if swap.new_density >= self.density:
                subset = self.subset
                self.clear()
                return subset
            else:
                self._swap_in_subset(swap)
        
        # In case we hit max steps
        subset = self.subset
        self.clear()
        return subset
