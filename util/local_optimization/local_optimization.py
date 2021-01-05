import networkx as nx
import numpy as np


class LocalOptimizer:
    def __init__(self):
        raise RuntimeError("This is an abstract class. Implement a subclass and make that version.")

    def optimize(self, initial: set, G: nx.Graph, max_steps: int) -> set:
        raise RuntimeError("This is an abstract class. Implement a subclass and call this function on that.")


def density_after_add(cur_density: float, subset_size: int, edges_in: int) -> float:
    return cur_density * (subset_size - 1) / (subset_size + 1) + 2 * (edges_in) / (subset_size * (subset_size + 1))

def density_after_rem(cur_density: float, subset_size: int, edges_in: int) -> float:
    return cur_density * subset_size / (subset_size - 2) - 2 * edges_in / ((subset_size-1) * (subset_size-2))

def density_after_swap(cur_density: float, subset_size: int, add_degree, rem_degree: int) -> float:
    return cur_density + ( 2 / (subset_size * (subset_size - 1)) * (add_degree - rem_degree) )

