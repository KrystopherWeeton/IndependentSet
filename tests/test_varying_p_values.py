from util.graph import *

gen = PerfectGraphGenerator(100)

for i in range(11):
    p = 10 * i / 100
    G, cheat = gen.generate_random_split_graph(p, False)
    max_clique_size = len(get_big_independent_set(nx.complement(G)))
    colors = len(set(nx.greedy_color(G, 'DSATUR').values()))
    print(f'p: {p} clique: {max_clique_size} cheat: {cheat} colors_found: {colors}')
