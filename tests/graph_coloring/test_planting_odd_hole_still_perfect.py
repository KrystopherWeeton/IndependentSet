from util.graph import *

G, cheat = PerfectGraphGenerator(1000).generate_random_split_graph(.5, True)

max_clique_size = len(get_big_independent_set(nx.complement(G)))
print(f'Pre planting: Clique is {max_clique_size}, colors is {cheat}')
for i in range(41):
    plant_random_hole_in_graph(G, 41, 0)
max_clique_size = len(get_big_independent_set(nx.complement(G)))
for i in range(41):
    colors = len(set(nx.greedy_color(G, 'random_sequential').values()))
    print(f'{max_clique_size} {colors}')

colors = len(set(nx.greedy_color(G, 'DSATUR').values()))
print(f'{max_clique_size} {colors}')
