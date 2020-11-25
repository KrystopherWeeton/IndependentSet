import networkx as nx
import random


# Generates an erdos_renyi graph with the provided # of vertices
# and edge probabilities.
def generate_erdos_renyi_graph(n: int, p: float) -> nx.Graph:
    return nx.erdos_renyi_graph(n=n, p=p)


# Generates an erdos_renyi graph with the preovided # of vertices
# and edge probabilities (p), with a planted subset of vertices
# that has the preovided edge probabilities (q). The vertices within
# the planted subset have key 'planted_key' attached to them.
def generate_planted_subset_graph(n: int, p: float, q: float, planted_size: int, planted_key: str) -> nx.Graph: 
    #? Perform initial checking to validate input
    if planted_size > n:
        raise RuntimeError(f"Attempt to generate a planted subset graph with {planted_size} vertices planted in a graph of size {n}")

    #? Generate internal and external graph and then join them.
    g: nx.Graph = nx.erdos_renyi_graph(n - planted_size, p)
    first_planted: int = n - planted_size + 1
    for i in range(first_planted, n):
        #TODO: Need to make it so the last 'planted_size' nodes are the planted ones
        g.add_node(i, attr=planted_key)
        # Add edges between planted and other portion
        for j in range(0, first_planted):
            if random.random() < p:
                g.add_edge(i, j)

        # Add edges within planted portion
        for j in range(first_planted, n):
            if random.random() < q:
                g.add_edge(i, j)
    
    return g


# Generates a planted independent set graph, similarly to the planted subset
# graph but with 0 edge probabilities within the planted subset
def generate_planted_independent_set_graph(n: int, p: float, planted_size: int, planted_key: str) -> nx.Graph:
    return generate_planted_subset_graph(n, p, 0, planted_size, planted_key)