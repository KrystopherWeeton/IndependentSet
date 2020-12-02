import networkx as nx

class LocalOptimizer:
    def __init__(self):
        raise RuntimeError("This is an abstract class. Implement a subclass and make that version.")

    def optimize(self, initial: set, G: nx.Graph, max_steps: int) -> set:
        raise RuntimeError("This is an abstract class. Implement a subclass and call this function on that.")



class BasicLocalOptimizer(LocalOptimizer):
    def __init__(self):
        pass

    def optimize(self, initial: set, G: nx.Graph, max_steps: int) -> set:
        # TODO: Implement the local optimization here
        return initial