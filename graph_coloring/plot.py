#!env/bin/python3
import click

from graph_coloring.plot_commands.plot_basic_heuristic import plot_basic_heuristic


@click.group()
def coloring():
    pass


coloring.add_command(plot_basic_heuristic)
if __name__ == "__main__":
    coloring()
