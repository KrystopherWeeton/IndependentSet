from util.results.results_dict import ResultsDict

d = ResultsDict()
d.add_dimension("n", [1, 2])
d.add_dimension("k", [1, 2])
d.add_dimension("t", [0, 1])

d.fix_dimensions()

d.add_result(1, n=1, k=1, t=0)
d.add_result(1, n=1, k=1, t=1)

d.add_result(2, n=2, k=2, t=1)
d.add_result(2, n=1, k=2, t=1)

print("HERE", d.results)

x = d.collapse_to_matrix()

print("NOW HERE", x)
