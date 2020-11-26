import networkx as nx
import numpy as np
import random

def metropolis_step(g: nx.Graph, temp: float, currState: list) -> list:
    # Choose a random vertex in V
    v_p = random.choice(nx.nodes(g))

    if v_p in currState:
        return currState if random.random() < (temp ** -1) else currState.pop(currState.index(v_p))
    else:
        make_bigger = True
        # Check if adding v gets a bigger independence set
        for v in currState:
            if v_p in nx.neighbors(g, v):
                make_bigger = False
                break
        # If we can make the independent set bigger, do so.
        return currState + [v_p] if make_bigger else currState 