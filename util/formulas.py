import statistics
from typing import List
import itertools

"""
    Calculates the density of a subset provided the current density, 
    subset size, and the degree (within the subset) of the vertex being added.
"""
def density_after_add(cur_density: float, subset_size: int, edges_in: int) -> float:
    return cur_density * (subset_size - 1) / (subset_size + 1) + 2 * (edges_in) / (subset_size * (subset_size + 1))


def density_after_rem(cur_density: float, subset_size: int, edges_in: int) -> float:
    if subset_size <= 2:
        raise Exception(f"Attempt to calculate density after removal for a subset of size {subset_size}")
    return cur_density * subset_size / (subset_size - 2) - 2 * edges_in / ((subset_size-1) * (subset_size-2))


def density_after_swap(cur_density: float, subset_size: int, add_degree, rem_degree: int) -> float:
    return cur_density + ( 2 / (subset_size * (subset_size - 1)) * (add_degree - rem_degree) )


"""
    Calculates the mean of a list of points. Wrapper around library.
"""
def mean(data: [float]) -> float:
    return statistics.mean(data)


"""
    Calculates the standard deviation of a list of points. Wrapper around library.
"""
def std_dev(data: [float]) -> float:
    return statistics.stdev(data)



"""
    Returns a list of all subsets of S of size m
"""
def subsets(S: set, m: int) -> List:
    return [set(s) for s in itertools.combinations(S, m)]