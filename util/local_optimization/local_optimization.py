import networkx as nx
import numpy as np


class Update:
    pass

class RemoveUpdate(Update):
    def __init__(self, new_density, node):
        self.new_density = new_density
        self.node = node

class AddUpdate(Update):
    def __init__(self, new_density, node):
        self.new_density = new_density
        self.node: int = node

class SwapUpdate(Update):
    def __init__(self, new_density, add_node, remove_node):
        self.new_density = new_density
        self.add_node = add_node
        self.remove_node = remove_node

class LocalOptimizer:
    def __init__(self):
        raise RuntimeError("This is an abstract class. Implement a subclass and make that version.")

        self.G: nx.Graph = None
        self.subset: set = None
        self.density: float = None
        self.subset_degree = None


    def optimize(self, initial: set, G: nx.Graph, max_steps: int) -> set:
        raise RuntimeError("This is an abstract class. Implement a subclass and call this function on that.")


    def _get_density(self) -> float:
        return nx.density(nx.subgraph(self.G, self.subset))


    def clear(self):
        self.G = None
        self.subset = None
        self.density = None
        self.subset_degree = None


    def _reset(self, G: nx.Graph, subset: set):
        self.G = G
        self.subset = subset
        self.density = self._get_density()
        self.subset_degree = [sum((1 for i in nx.edge_boundary(G, set([v]), self.subset))) for v in G.nodes]


    def _get_best_remove(self) -> RemoveUpdate:
        remove_index: int = max(self.subset, key = lambda j : self.subset_degree[j])
        remove_degree = self.subset_degree[remove_index]
        new_density: float = density_after_rem(self.density, len(self.subset), remove_degree)
        return RemoveUpdate(new_density, remove_index)

    
    def _get_best_add(self) -> AddUpdate:
        add_index = np.argmin([float('inf') if j in self.subset else self.subset_degree[j] for j in self.G.nodes])
        new_density: float = density_after_add(self.density, len(self.subset), self.subset_degree[add_index])
        return AddUpdate(new_density, add_index)

    def _get_best_swap(self) -> SwapUpdate:
        remove: RemoveUpdate = self._get_best_remove()
        add: AddUpdate = self._get_best_add()
        new_density: float = density_after_swap(self.density, len(self.subset), self.subset_degree[add.node], self.subset_degree[remove.node])
        return SwapUpdate(new_density, add.node, remove.node)

    
    def _add_to_subset(self, add: AddUpdate):
        if add.node in self.subset:
            raise RuntimeError("ERROR: Request to add node already in subset to subset.")
            
        self.subset.add(add.node)
        for neighbor in self.G.neighbors(add.node):
            self.subset_degree[neighbor] += 1
        self.density = add.new_density
    

    def _remove_from_subset(self, remove: RemoveUpdate):
        if remove.node not in self.subset:
            raise RuntimeError("ERROR: Removed node not in subset")
        self.subset.remove(remove.node)
        for neighbor in self.G.neighbors(remove.node):
            self.subset_degree[neighbor] -= 1
        self.density = remove.new_density


    def _swap_in_subset(self, swap: SwapUpdate):
        self._add_to_subset(AddUpdate(-1, swap.add_node))
        self._remove_from_subset(RemoveUpdate(swap.new_density, swap.remove_node))


def density_after_add(cur_density: float, subset_size: int, edges_in: int) -> float:
    return cur_density * (subset_size - 1) / (subset_size + 1) + 2 * (edges_in) / (subset_size * (subset_size + 1))

def density_after_rem(cur_density: float, subset_size: int, edges_in: int) -> float:
    return cur_density * subset_size / (subset_size - 2) - 2 * edges_in / ((subset_size-1) * (subset_size-2))

def density_after_swap(cur_density: float, subset_size: int, add_degree, rem_degree: int) -> float:
    return cur_density + ( 2 / (subset_size * (subset_size - 1)) * (add_degree - rem_degree) )

