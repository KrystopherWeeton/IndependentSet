import networkx as nx
import numpy as np

DEBUG_PRINT: bool = True

class LocalOptimizer:
    def __init__(self):
        raise RuntimeError("This is an abstract class. Implement a subclass and make that version.")

    def optimize(self, initial: set, G: nx.Graph, max_steps: int) -> set:
        raise RuntimeError("This is an abstract class. Implement a subclass and call this function on that.")



class BasicLocalOptimizer(LocalOptimizer):
    def __init__(self):
        pass

    def __get_density(self, G: nx.Graph, subset: set) -> float:
        return nx.density(nx.subgraph(G, subset))

    def optimize(self, initial: set, G: nx.Graph, max_steps: int) -> set:
        # Pre-process and store some results
        nodes: set = set(G.nodes)
        subset: set = initial

        for i in range(max_steps):
            starting_density = self.__get_density(G, subset)

            #? Get the best vertex to add / remove from the graph
            k: int = len(subset)
            edge_boundary = [
                sum((1 for i in nx.edge_boundary(
                G,
                set([v]),
                subset)))
                for v in nodes
            ]
            add_index = np.argmin([float('inf') if i in subset else edge_boundary[i] for i in nodes])
            add_degree = edge_boundary[add_index]

            # TODO: Go through and make sure we are pulling from the correct vertices
            rem_index = np.argmax([-1 if i not in subset else edge_boundary[i] for i in nodes])
            rem_degree = edge_boundary[rem_index]

            add_density: float = (starting_density * k * (k-1) + add_degree) / (k * (k+1))
            rem_density: float = (starting_density * k * (k - 1) - rem_degree) / ((k - 1) * (k - 2))

            # Split into cases based on density
            if add_density >= starting_density and rem_density >= starting_density:
                # print('returned')
                return subset
            else:
                # One of them is smaller
                if add_density < rem_density:
                    subset.add(add_index)
                else:
                    # print("rem", rem_density, starting_density)
                    subset.remove(rem_index)

        # We ran out of steps, return what we have right now
        if DEBUG_PRINT:
            print(
                f"Warning: Local optimization ran {max_steps} steps without hitting a local optimum."
                " Consider increasing the maximum number of steps to find local optimums.")
        return subset
