import networkx as nx
import random
import itertools
import numpy as np


# Returns a list of nodes in a random 'headstart' set of size l with k nodes inside the independence set
def get_overlap_set(l: int, k: int, g: nx.graph, planted_key: str) -> list:
    planted: list = nx.get_node_attributes(g, planted_key)
    intersection: list = random.sample(planted, k)
    disjoint = random.sample(set(nx.nodes(g)).difference(intersection))
    return disjoint + intersection

# Generates an erdos_renyi graph with the provided # of vertices
# and edge probabilities.
def generate_erdos_renyi_graph(n: int, p: float) -> nx.Graph:
    return nx.erdos_renyi_graph(n=n, p=p)


# Generates an erdos_renyi graph with the preovided # of vertices
# and edge probabilities (p), with a planted subset of vertices
# that has the preovided edge probabilities (q). The vertices within
# the planted subset have key 'planted_key' attached to them.
def generate_planted_subset_graph(n: int, p: float, q: float, planted_size: int, planted_key: str)-> (nx.Graph, list): 
    #? Perform initial checking to validate input
    if planted_size > n:
        raise RuntimeError(f"Attempt to generate a planted subset graph with {planted_size} vertices planted in a graph of size {n}")

    #? Generate original graph and sample planted set from nodes
    g: nx.Graph = nx.erdos_renyi_graph(n, p)
    planted: list = random.sample(nx.nodes(g), planted_size)
    
    #? Remove edges from the planted set
    planted_edges: list = list(itertools.combinations(planted, 2))
    g.remove_edges_from(planted_edges)
    # print(g, dict.fromkeys(planted, planted_key))
    # nx.set_node_attributes(g, dict.fromkeys(planted, {planted_key}))
    
    #? Put back the edges with probability q
    for e in planted_edges:
        if random.random() < q:
            g.add_edge(e)

    return g, planted


# Generates a planted independent set graph, similarly to the planted subset
# graph but with 0 edge probabilities within the planted subset
def generate_planted_independent_set_graph(n: int, p: float, planted_size: int, planted_key: str) -> (nx.Graph, list):
    return generate_planted_subset_graph(n, p, 0, planted_size, planted_key)