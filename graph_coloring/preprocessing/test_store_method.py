import gc

# import hickle as hkl
import klepto
import networkx as nx

# import h5py

dic = {}
for i in range(10):
    print(f'graph {i}')
    dic[i] = (301, nx.erdos_renyi_graph(3015, .5))
    gc.collect()
k = klepto.archives.dir_archive('memo_after_deleting', dic)
gc.collect()
print('loaded archive')
# k.dump()
for i, key in enumerate(dic.keys()):
    print(dic[key])
    print(f'dumping {i}')
    k.dump(key)
    gc.collect()
    print('finished this one')

# hkl.dump(dic, 'test.hkl', mode='w')
# print('dumped successfully')
# hkl.load('test.hkl')
