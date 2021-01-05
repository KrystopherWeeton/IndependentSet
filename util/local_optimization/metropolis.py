from util.local_optimization.local_optimization import LocalOptimizer, density_after_add, density_after_rem, density_after_swap
import networkx as nx
import numpy as np
import random
import math

class AllLocalOptimizer(LocalOptimizer):
    def __init__(self, temperature):
        self.T = temperature
        pass


    def _get_density(self) -> float:
        return nx.density(nx.subgraph(self.G, self.subset))


    def _calc_threshold(self, density: float) -> float:
        return math.e**(-density / self.T)


    def _reset(self, G: nx.Graph, initial_subset: set):
        # Reset G, cross edges, and subset
        self.G = G
        self.subset = initial_subset
        self.density = self._get_density()
        self.cross_edges = [sum((1 for i in nx.edge_boundary(G, set([v]), self.subset))) for v in G.nodes]

    
    def _add_to_subset(self, node: int, new_density: float):
        if node in self.subset:
            raise RuntimeError("ERROR: Added node in subset")
        self.subset.add(node)
        # Update cross edges
        for neighbor in self.G.neighbors(node):
            self.cross_edges[neighbor] += 1


    def _rem_from_subset(self, node: int, new_density: float):
        if node not in self.subset:
            raise RuntimeError("ERROR: Removed node not in subset")
        self.subset.remove(node)
        for neighbor in self.G.neighbors(node):
            self.cross_edges[neighbor] -= 1

        #? Update density tracker
        self.density = new_density
        pass
    

    def optimize(self, initial: set, G: nx.Graph, max_steps: int) -> set:
        # Pre-process and store some results
        self._reset(G, initial)

        for i in range(max_steps):
            k: int = len(self.subset)

            #? Generate a candidate, calculate new density
            node: int = random.choice(G.nodes)
            in_subset: bool = node in self.subset
            degree_in_subset: int = self.cross_edges[node]
            new_density: float = density_after_rem(self.density, k, degree_in_subset) if in_subset else density_after_add(self.density, k, degree_in_subset)


            #? Calculate acceptance threshold, determine action
            threshold: float = self._calc_threshold(new_density)
            if random.random() <= threshold:
                if in_subset:
                    self._rem_from_subset(node, new_density)
                else:
                    self._add_to_subset(node, new_density)
           

        # We ran out of steps, return what we have right now
        print(
            f"Warning: Local optimization ran {max_steps} steps without hitting a local optimum."
            " Consider increasing the maximum number of steps to find local optimums.")
        return subset
