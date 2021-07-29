#!env/bin/python3
import click

from graph_coloring.experiments.basic_heuristic import basic_heuristic
from graph_coloring.experiments.glauber_dynamics import glauber_dynamics


@click.group()
def coloring():
    pass


coloring.add_command(basic_heuristic)
coloring.add_command(glauber_dynamics)

if __name__ == "__main__":
    coloring()