from util.local_optimization.local_optimization import LocalOptimizer, density_after_add, density_after_rem, density_after_swap
import networkx as nx
import numpy as np

class AllLocalOptimizer(LocalOptimizer):
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


    def _swap_in_subset(self, add: int, rem: int, new_density: float):
        #? Perform checks to verify there are no major issues
        if add in self.subset:
            raise RuntimeError("ERROR: Adding node in subset.")
        if rem not in self.subset:
            raise RuntimeError("ERROR: Removed node not in subset")

        #? Swap the nodes, update density
        self.subset.add(add)
        self.subset.remove(rem)
        self.density = new_density

        #? Update cross edges tracker 
        for neighbor in self.G.neighbors(add):
            self.cross_edges[neighbor] += 1
        for neighbor in self.G.neighbors(rem):
            self.cross_edges[neighbor] -= 1


    def optimize(self, initial: set, G: nx.Graph, max_steps: int) -> set:
        # Pre-process and store some results
        self._reset(G, initial)
        
        for i in range(max_steps):
            #? Get the best vertex to add / remove from the graph
            k: int = len(self.subset)
            # TODO: Is the best swap the best add and best remove?

            #? Get the best index to add to the subset
            add_index = np.argmin([float('inf') if i in self.subset else self.cross_edges[i] for i in G.nodes])
            add_degree = self.cross_edges[add_index] if i not in self.subset else float('inf')

            #? Get the best index to remove from the subset
            rem_index = np.argmax([-1 if i not in self.subset else self.cross_edges[i] for i in G.nodes])
            rem_degree = self.cross_edges[rem_index] if i in self.subset else -1

            #? Calculate new density and check if we are at a local optimum
            add_density: float = density_after_add(self.density, k, add_degree)
            rem_density: float = density_after_rem(self.density, k, rem_degree)
            swap_density: float = density_after_swap(self.density, k, add_degree=add_degree, rem_degree=rem_degree)
            min_density: float = min(add_density, rem_density, swap_density)

            #? Stop at a local optimum
            if min_density >= self.density:
                return self.subset

            #? Update subset appropriately
            if add_density < rem_density and add_density < swap_density:
                self._add_to_subset(add_index, add_density)
            elif rem_density < add_density and rem_density < swap_density:
                self._rem_from_subset(rem_index, rem_density)
            else:
                # Implicit rem_density is the smallest
                self._swap_in_subset(add_index, rem_index, swap_density)

        # We ran out of steps, return what we have right now
        print(
            f"Warning: Local optimization ran {max_steps} steps without hitting a local optimum."
            " Consider increasing the maximum number of steps to find local optimums.")
        return self.subset
