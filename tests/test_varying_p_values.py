import mpmath
from tqdm import tqdm

from util.graph import *

n = 500
gen = PerfectGraphGenerator(n)
ln_n = round(mpmath.ln(n))
for co_split in [True, False]:
    for i in range(10):
        p = 10 * i / 100
        print(f'Working with p: {p}')

        for planted in tqdm(range(ln_n, n, ln_n)):
            gc.collect()
            try:
                G, cheat = gen.generate_random_split_graph(p, co_split, planted)
            except AttributeError:
                # print('Failed to generate the graph due to some foreseeable reasons, continuing')
                continue

            max_clique_size = len(get_big_independent_set(nx.complement(G)))
            colors = len(set(nx.greedy_color(G, 'DSATUR').values()))
            if cheat != colors:
                print(f'p: {p} clique: {max_clique_size} cheat: {cheat} colors_found: {colors}')
                print('DSATUR failed to find optimal coloring, damn, that is sad')
