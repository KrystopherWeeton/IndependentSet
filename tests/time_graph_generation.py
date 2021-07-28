import time

from util.graph import PerfectGraphGenerator

print("starting")
start = time.time()
PerfectGraphGenerator(n=1000, p=.5, co_split=False).generate_random_split_graph()
print("finished", time.time() - start)
