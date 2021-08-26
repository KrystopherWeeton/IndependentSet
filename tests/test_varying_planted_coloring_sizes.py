from util.graph import *

gen = PerfectGraphGenerator(1000)

for i in range(1, 10):
    G, cheat = gen.generate_random_split_graph((75 + i) / 100, False, 20)
    max_clique_size = len(get_big_independent_set(nx.complement(G)))
    colors = len(set(nx.greedy_color(G, 'DSATUR').values()))
    print(f'mult: {i} clique: {max_clique_size} cheat: {cheat} colors_found: {colors}')
