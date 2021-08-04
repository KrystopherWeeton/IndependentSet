#!env/bin/python3
import click

from graph_coloring.experiments.basic_heuristic import basic_heuristic
from graph_coloring.experiments.basic_local_search import basic_local_search
from graph_coloring.experiments.glauber_dynamics import glauber_dynamics


@click.group()
def coloring():
    pass


coloring.add_command(basic_heuristic)
coloring.add_command(glauber_dynamics)
coloring.add_command(basic_local_search)

if __name__ == "__main__":
    coloring()