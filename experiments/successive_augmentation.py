#!env/bin/python3
import click
import math
import util.storage as storage
from util.results.size_results import SizeResults, generate_size_results_file_name
from util.graph import generate_planted_independent_set_graph
from util.heuristics.fixed_gww import FixedGWW
from util.storage import store
import copy

def planted_ind_set_size(n: int) -> int:
    return math.ceil(math.sqrt(n)) * 1

EDGE_PROBABILITY: float = 0.5

BASE_METADATA: dict = {
}

"""
    Experiment which attempts to solve a planted clique problem from start to end.
"""
@click.command()
def successive_augmentation():
    pass