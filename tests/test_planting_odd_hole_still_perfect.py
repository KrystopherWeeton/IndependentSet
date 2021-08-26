from util.graph import *

G, cheat = PerfectGraphGenerator(1000, .5, True).generate_random_split_graph()
plant_random_hole_in_graph(G, 999, 0)
print(f'{len(get_big_independent_set(nx.complement(G)))} {len(set(nx.greedy_color(G).values()))}')
