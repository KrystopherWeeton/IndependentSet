from queue import SimpleQueue
from typing import Dict, List, Set

import networkx as nx

from util.misc import validate
from util.models.instance import Instance
from util.models.solution import Solution
from util.new_graph.models.graph import Graph


def map_entire_search_space(instance: Instance, seed: Solution) -> Graph:
    q: SimpleQueue = SimpleQueue()
    q.put()
    pass

def bfs_map_search_space(instance: Instance, max_steps: int) -> Graph:
    pass



def bfs(instance: Instance, seed: Solution, max_steps: int) -> Graph:
    q: SimpleQueue = SimpleQueue()
    g: nx.Graph = nx.empty_graph()
    graph_map: Dict[Solution, int] = {}
    explored: Set = set()
    validate(instance.validate_solution_type(seed), "Solution provided has the incorrect type")
    q.put(seed)
    while not q.empty():
        s: Solution = q.get()
        # Add s if not already present in (in memory) graph
        if s not in graph_map:
            g.add_node(score=instance.metric(s))
            graph_map[s] = g.number_of_nodes() - 1
        for n in instance.neighbors(s):
            # Add n if not already present in (in memory) graph
            if n not in graph_map:
                g.add_node(score=instance.metric(n))
                graph_map[n] = g.number_of_nodes() - 1
            # Add edge into graph (if not already present)
            g.add_edge(graph_map[n], graph_map[s])
            if n not in explored:
                q.put(n)
        explored.add(s) 
