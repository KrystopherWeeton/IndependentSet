import networkx as nx
import numpy as np

from util.local_optimization.local_optimization import (LocalOptimizer,
                                                        density_after_add,
                                                        density_after_rem)


class BasicLocalOptimizer(LocalOptimizer):
    def __init__(self):
        pass

    def _get_density(self) -> float:
        return nx.density(nx.subgraph(self.G, self.subset))


    def _reset(self, G: nx.Graph, initial_subset: set):
        # Reset G, cross edges, and subset
        self.G = G
        self.subset = initial_subset
        self.density = self._get_density()
        self.cross_edges = [sum((1 for i in nx.edge_boundary(G, set([v]), self.subset))) for v in G.nodes]


    def _update_subset(self, node: int, adding: bool, new_density: float):
        #? Update subset and cross edges
        if adding:
            if node in self.subset:
                raise RuntimeError("ERROR: Added node in subset")
            self.subset.add(node)
            # Update cross edges
            for neighbor in self.G.neighbors(node):
                self.cross_edges[neighbor] += 1
        else:
            if node not in self.subset:
                raise RuntimeError("ERROR: Removed node not in subset")
            self.subset.remove(node)
            for neighbor in self.G.neighbors(node):
                self.cross_edges[neighbor] -= 1

        #? Update density tracker
        self.density = new_density


    def optimize(self, initial: set, G: nx.Graph, max_steps: int) -> set:
        # Pre-process and store some results
        self._reset(G, initial)
        
        for i in range(max_steps):
            #? Get the best vertex to add / remove from the graph
            k: int = len(self.subset)
            # TODO: Triple check that optimize is actually working correctly

            # Get the best index to add to the subset
            add_index = np.argmin([float('inf') if i in self.subset else self.cross_edges[i] for i in G.nodes])
            add_degree = self.cross_edges[add_index] if i not in self.subset else float('inf')

            # Get the best index to remove from the subset
            rem_index = np.argmax([-1 if i not in self.subset else self.cross_edges[i] for i in G.nodes])
            rem_degree = self.cross_edges[rem_index] if i in self.subset else -1

            # Calculate new densities using closed form
            add_density = density_after_add(self.density, k, add_degree)
            rem_density = density_after_rem(self.density, k, rem_degree)

            #? Split into cases based on density and update subset
            if add_density >= self.density and rem_density >= self.density:
                # print(f"Found a local optimum with density {self._get_density()} with l={len(self.subset)} nodes out of {len(G.nodes)} total nodes.")
                return self.subset
            else:
                if rem_density < add_density:
                    node, density = rem_index, rem_density
                else:
                    node, density = add_index, add_density
                self._update_subset(node, add_density < rem_density, density)
                #print(f"Updated {node} to set. New size is {len(self.subset)}. New density is {self.__get_density(G, subset)}")

        # We ran out of steps, return what we have right now
        print(
            f"Warning: Local optimization ran {max_steps} steps without hitting a local optimum."
            " Consider increasing the maximum number of steps to find local optimums.")
        return subset


