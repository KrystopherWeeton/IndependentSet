import networkx as nx
import numpy as np
import random

# Right now very simple, just return a random vertex (unless we start with hint)
def get_init_state(g: nx.Graph, ) -> set:
    return set(random.choice(nx.nodes(g)))


def metropolis_step(g: nx.Graph, temp: float, currState: set) -> set:
    # Choose a random vertex in V
    v_p = random.choice(nx.nodes(g))

    if v_p in currState:
        return currState if random.random() < (temp ** -1) else currState.discard(v_p)
    else:
        make_bigger = True
        # Check if adding v gets a bigger independence set
        for v in currState:
            if v_p in nx.neighbors(g, v):
                make_bigger = False
                break
        # If we can make the independent set bigger, do so.
        if make_bigger:
            currState.add(v_p)
        return currState