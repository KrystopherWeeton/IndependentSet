import gc

import hickle as hkl
import networkx as nx

dic = {}
for i in range(5):
    print(f'graph {i}')
    dic[i] = (0, nx.erdos_renyi_graph(3015, .5))
    gc.collect()

hkl.dump(dic, 'test.hkl', mode='w')
hkl.load('test.hkl')
