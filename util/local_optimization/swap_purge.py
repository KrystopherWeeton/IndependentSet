from util.local_optimization.local_optimization import *
import networkx as nx
import numpy as np


class SwapPurgeLocalOptimizer(LocalOptimizer):
    def __init__(self):
        pass


    def swap(self, max_steps: int):
        for i in range(max_steps):
            swap: SwapUpdate = self._get_best_swap()
            if swap.new_density >= self.density:
                return
            else:
                self._swap_in_subset(swap)
    

    def remove(self, max_steps: int):
        for i in range(max_steps):
            remove: RemoveUpdate = self._get_best_remove()
            if remove.new_density >= self.density:
                return
            else:
                self._remove_from_subset(remove)


    def optimize(self, initial: set, G: nx.Graph, max_steps: int) -> set:
        self._reset(G, initial)
        self.swap(max_steps)
        self.remove(max_steps)
        subset: set = self.subset
        self.clear()
        return subset
        
        