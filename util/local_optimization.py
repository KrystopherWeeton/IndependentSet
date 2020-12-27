import networkx as nx
import numpy as np


class LocalOptimizer:
    def __init__(self):
        raise RuntimeError("This is an abstract class. Implement a subclass and make that version.")

    def optimize(self, initial: set, G: nx.Graph, max_steps: int) -> set:
        raise RuntimeError("This is an abstract class. Implement a subclass and call this function on that.")


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
            # print(f"Density={self.density}, k={k}, add_degree={add_degree}, rem_degree={rem_degree}")
            add_density: float = (self.density * k * (k-1) + add_degree) / (k * (k+1))
            rem_density: float = (self.density * k * (k - 1) - rem_degree) / ((k - 1) * (k - 2))

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



class SwapLocalOptimizer(LocalOptimizer):
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


    def _update_subset(self, add: int, rem: int, new_density: float):
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
            # TODO: Check that this density is correct (first time working on this a little bit)
            new_density: float = self.density + (2 / (k(k-1)) ) (add_degree - rem_degree);
            if new_density >= self.density:
                return self.subset
            else:
                self._update_subset(add_index, rem_index, new_density)

        # We ran out of steps, return what we have right now
        print(
            f"Warning: Local optimization ran {max_steps} steps without hitting a local optimum."
            " Consider increasing the maximum number of steps to find local optimums.")
        return subset

class SwapLocalOptimizer(LocalOptimizer):
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


    def _update_subset(self, add: int, rem: int, new_density: float):
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
            # TODO: Check that this density is correct (first time working on this a little bit)
            new_density: float = self.density + (2 / (k(k-1)) ) (add_degree - rem_degree);
            if new_density >= self.density:
                return self.subset
            else:
                self._update_subset(add_index, rem_index, new_density)

        # We ran out of steps, return what we have right now
        print(
            f"Warning: Local optimization ran {max_steps} steps without hitting a local optimum."
            " Consider increasing the maximum number of steps to find local optimums.")
        return subset
