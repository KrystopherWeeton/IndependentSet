import time

from util.graph import PerfectGraphGenerator

print("starting")
start = time.time()
PerfectGraphGenerator(n=1000).generate_random_split_graph(.5, False)
print("finished", time.time() - start)
