#!env/bin/python3
import click

from graph_coloring.experiments.basic_heuristic import basic_heuristic
from graph_coloring.experiments.basic_local_search import basic_local_search
from graph_coloring.experiments.glauber_dynamics import glauber_dynamics
from graph_coloring.experiments.k_gww import k_gww
from graph_coloring.preprocessing.preprocessing import preprocessing


@click.group()
def coloring():
    pass


coloring.add_command(basic_heuristic)
coloring.add_command(glauber_dynamics)
coloring.add_command(basic_local_search)
coloring.add_command(preprocessing)
coloring.add_command(k_gww)
if __name__ == "__main__":
    coloring()